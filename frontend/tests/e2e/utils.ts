import db from "../db_data.json" with { type: "json" };
import messages from "../../src/messages.json" with { type: "json" };


const isPlainObject: Function = (o: any) => Boolean(
  o && o.constructor && o.constructor.prototype && o.constructor.prototype.hasOwnProperty("isPrototypeOf")
);
const flattenObject: Function = (obj: any, keys = []) => {
  return Object.keys(obj).reduce((acc: any, key: any) => {
    return Object.assign(acc, isPlainObject(obj[key])
      ? flattenObject(obj[key], keys.concat(key))
      : { [keys.concat(key).join(".")]: obj[key] }
    )
  }, {})
}

export const t = (() => {
  const en = flattenObject(messages["en"]);
  return (key: string) => {
    return en[key];
  }
})()


export function beforeEachHook(page) {

    const {
      assets, assets_state, assets_values, categories, classes, config, portfolio, structures, structure_categories
    } = JSON.parse(JSON.stringify(db));

    return async () => {
      await page.route(/\/config\/?(\.*)/, async route => {
        const m = (/\/config\/?(\.*)/).exec(route.request().url());
        if (!m || m.length < 2) {
          await route.continue();
          return
        }
        if (m[1] === "") {
          await route.fulfill({ json: { data: config }});
        } else {
          const index = config.findIndex(c => c.config_name === "currency");
          if (route.request().method() === "PUT") {
            config[index].config_value = route.request().postDataJSON().config_value;
          }
          await route.fulfill({ json: config[index] });
        }
      });

      await page.route(/\/portfolio/, async route => {
        await route.fulfill({ json: { data: portfolio }});
      });

      await page.route(/\/assets\/state/, async route => {
        await route.fulfill({ json: { data: assets_state }});
      });

      await page.route(/\/assets\/values/, async route => {
        await route.fulfill({ json: { data: assets_values }});
      });

      await page.route(/\/assets$/, async route => {
        await route.fulfill({ json: { data: assets }});
      });

      await page.route(/\/categories/, async route => {
        await route.fulfill({ json: { data: categories }});
      });

      await page.route(/\/classes\/?(\d*)/, async route => {
        const m = (/\/classes\/?(\d*)/).exec(route.request().url());
        if (!m || m.length < 2) {
          await route.continue();
          return
        }
        if (m[1] !== "") {
          const class_id = parseInt(m[1]);
          const method = route.request().method();
          if (method === "DELETE") {
            if (class_id < 4) {
              await route.fulfill({ status: 500, json: { detail: "FOREIGN KEY constraint_failed" }});
              return
            }
            classes.splice(classes.findIndex(c => c.class_id === class_id), 1);
            await route.fulfill({ status: 204 });
            return
          } else if (method === "PUT") {
            const class_name = route.request().postDataJSON().class_name;
            if (classes.filter(c => c.class_name === class_name && c.class_id !== class_id).length > 0) {
              await route.fulfill({ status: 500, json: { detail: "UNIQUE constraint failed" }});
              return
            }
            classes[classes.findIndex(c => c.class_id === class_id)] = {class_id, class_name};
            await route.fulfill({ json: classes.filter(c => c.class_id === class_id) });
          }
        } else {
          if (route.request().method() === "POST") {
            const class_name = route.request().postDataJSON().class_name;
            if (classes.filter(c => c.class_name === class_name).length > 0) {
              await route.fulfill({ status: 500, json: { detail: "UNIQUE constraint failed" }});
              return
            }
            const class_id = classes.length + 1;
            classes.push({ class_id, class_name });
            await route.fulfill({status: 201, json: classes.filter(c => c.class_id === class_id) });
            return
          }
          await route.fulfill({ json: { data: classes }});
        }
      });

      await page.route(/\/structures\/?(\d*)/, async route => {
        const m = (/\/structures\/?(\d*)/).exec(route.request().url());
        if (!m || m.length < 2) {
          await route.continue();
          return
        }
        if (m[1] !== "") {
          const structure_id = parseInt(m[1]);
          if (route.request().method() === "PATCH") {
            structures.forEach(s => {
              s.is_current = s.structure_id === structure_id;
            });
            await route.fulfill({ status: 200 });
          } else {
            await route.fulfill({ json: { data: structure_categories.filter(s => s.structure_id === structure_id) }});
          }
        } else {
          await route.fulfill({ json: { data: structures }});
        }
      });

      await page.goto("/");
    };

}
