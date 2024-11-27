<template>
  <v-dialog
    max-width="600px"
    v-model="opened"
  >
    <v-card
      class="pa-3"
    >
      <v-card-title
        class="ms-2"
        data-testid="delete-confirmation-dialog-title"
      >
        {{ t("confirmations.title") }}
      </v-card-title>
      <v-card-text>
        <div
          class="mb-2"
          data-testid="delete-confirmation-dialog-text"
        >
          {{ text }}
        </div>
        <div
          class="mb-3"
          data-testid="delete-confirmation-dialog-confirm-text"
        >
          {{ t("confirmations.delete_confirm") }}
        </div>
        <v-text-field
          data-testid="delete-confirmation-dialog-input"
          density="compact"
          hide-details
          required
          v-model="confirmationString"
        >
          <template v-slot:label>
            delete <span class="ms-1 warning">*</span>
          </template>
        </v-text-field>
      </v-card-text>
      <v-card-actions
        class="pe-4 me-2"
      >
        <v-spacer />
        <v-btn
          color="primary"
          data-testid="delete-confirmation-dialog-delete-button"
          :disabled="confirmationString !== 'delete'"
          @click="$emit('delete')"
        >
          {{ t("buttons.delete") }}
        </v-btn>
        <v-btn
          @click="$emit('close')"
        >
          {{ t("buttons.cancel") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { t } from "@/common/locale";
import { defineComponent } from "vue";


export default defineComponent({
  computed: {
    t() {
      return t;
    },
  },
  emits: ["close", "delete"],
  props: {
    text: {
      type: String,
      required: true,
    },
    opened: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      confirmationString: "",
    };
  },
  watch: {
    opened(value) {
      if (value) {
        this.confirmationString = "";
      }
    },
  },
});
</script>
