export interface ConfigEntry {
  /*
  Interface representing a configuration entry.

  Attributes:
      config_name (string | null): The name of the configuration entry.
      config_value (any): The value of the configuration entry.
  */
  config_name?: string | null;
  config_value: any;
}
