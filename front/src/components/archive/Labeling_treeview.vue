<template>
  <v-col cols="12">
    <v-card tile class="temp">
      
      <h3 class="instruction"> ## Which label best describes the <span class="blue-text">selected box(es)</span>? </h3>
      <v-card-text> 
        <v-row>
          <v-col>
            <v-treeview
              v-model="selection"
              :items="items"
              selection-type="leaf"
              selectable
              return-object
              open-on-click
              open-all
              dense
            ></v-treeview>
          </v-col>
          <v-divider vertical></v-divider>
          <v-col class="pa-6" cols="6">
            <template v-if="!selection.length">
              No nodes selected.
            </template>
            <template v-else>
              <div v-for="node in selection" :key="node.id">
                {{ node.parentname }} / 
                {{ node.name }}
              </div>
            </template>
          </v-col>
        </v-row>
        <br/>
        <v-btn @click="labelSelected" :disabled="emptySelection"> RECORD </v-btn>
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
      selectionType: 'leaf',
      selection: [],
      items: [
        { 
          id: 1, 
          name: 'menu',
          children: [
            { id: 2, name: 'menu.name', parentname: 'menu' },
            { id: 3, name: 'menu.unit_price', parentname: 'menu'},
            { id: 4, name: 'menu.count', parentname: 'menu'},
            { id: 5, name: 'menu.price', parentname: 'menu'},
          ],
        },
        {
          id: 6,
          name: 'subtotal',
          children: [
            { id: 7, name: 'subtotal.subtotal_price', parentname: 'subtotal' },
            { id: 8, name: 'subtotal.tax_price', parentname: 'subtotal' },
          ],
        },
        { 
          id: 9, 
          name: 'total',
          children: [
            { id: 10, name: 'total.total_price', parentname: 'total' },
            { id: 11, name: 'total.cash_price', parentname: 'total' },
            { id: 11, name: 'total.credit_card_price', parentname: 'total' },
            { id: 11, name: 'total.change_price', parentname: 'total' },
          ],
        },
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
      return !(this.selection.length === 1)
    }
  },

  methods: {
    ...mapActions(['updateImageBoxes']),
    ...mapGetters(['getImageBoxes']),
    labelSelected: function() {
      this.getImageBoxes()
      const imageBox = this.image_box
      //const selectedBoxes = this.image_box.filter(v => v.selected === true)
      const label = this.selection[0].name
      
      for (var box in imageBox) {
        if (imageBox[box].selected === true) {
          this.image_box[box].label = label
          this.image_box[box].selected = false
          this.image_box[box].annotated = true
        }
      }

      this.updateImageBoxes(this.image_box)
      this.selection = []

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

</style>