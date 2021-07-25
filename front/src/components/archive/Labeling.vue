<template>
  <v-col cols="12">
    <v-card tile class="temp">
      
      <h3 class="instruction"> ## Which label best describes the <span class="blue-text">selected box(es)</span>? </h3>
      <v-card-text> 
        <v-row>
          <v-col>
            <v-radio-group
              v-model="selection"
              hide-details
            >
            <v-radio v-for="item in items" 
                    :key="item.id"
                    :label="item.name"
                    :value="item.name"/>

            </v-radio-group>
          </v-col>
        </v-row>
        <v-divider/>
        <br>
        <v-row justify="start">
          <v-btn @click="labelSelected" :disabled="emptySelection" class="btn"> RECORD </v-btn>
        </v-row>
      </v-card-text>

    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Labeling',
  data() {
    return {
      selection: null,
      items: [
        { id: 1, name: 'menu.name'},
        { id: 2, name: 'menu.unit_price'},
        { id: 3, name: 'menu.count'},
        { id: 4, name: 'menu.price'},
        { id: 5, name: 'subtotal.subtotal_price'},
        { id: 6, name: 'subtotal.tax_price'},
        { id: 7, name: 'total.total_price'},
        { id: 8, name: 'total.cash_price'},
        { id: 9, name: 'total.credit_card_price'},
        { id: 10, name: 'total.change_price'},
        { id: 11, name: 'N/A (Not Applicable)'}
      ],
      selected_boxes: this.$store.getters.getSelectedBoxes,
      image_box: this.$store.getters.getImageBoxes,
    }
  },

  mounted: function () {
    this.image_box = this.$store.getters.getImageBoxes

    this.$store.subscribeAction((action) => {
      if (action.type === "updateImageBoxes") {
        this.image_box = this.$store.getters.getImageBoxes
      }
    }),
    this.$store.subscribe((getters) => {
      if (getters.type === "getSelectedBoxes") {
        this.selected_boxes = this.$store.getters.getSelectedBoxes
      }
    })
  },

  computed: {
    emptySelection() {
      return (this.selection === null)
    }
  },

  methods: {
    ...mapActions(['updateImageBoxes']),
    ...mapGetters(['getImageBoxes']),
    labelSelected: function() {
      this.getImageBoxes()
      const imageBox = this.image_box
      //const selectedBoxes = this.image_box.filter(v => v.selected === true)
      const label = this.selection
      
      for (var box in imageBox) {
        if (imageBox[box].selected === true) {
          this.image_box[box].label = label
          this.image_box[box].selected = false
          this.image_box[box].annotated = true
        }
      }

      this.updateImageBoxes(this.image_box)
      this.selection = null

    }
  },
}
</script>
<style scoped>
.temp {
  margin-top: 1em;
}
.instruction {
  text-align: left;
  padding-left: 20px;
}
.blue-text {
  color:blue;
  font-weight: bold;
}
.btn {
  margin-left: 1rem;
}

</style>