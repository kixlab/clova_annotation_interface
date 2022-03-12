<template>
  <v-tooltip bottom :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :disabled="disabled"
        color="green"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Check answer
      </v-btn>
      </div>
    </template>
    Annotate all boxes to check answer!
  </v-tooltip>
</template>

<script>
import {mapGetters, mapActions} from 'vuex';

export default {
  name: "SubmitButton",
  methods: {
    ...mapGetters(['getIfAllImagesAnnotated']),
    ...mapActions(['updateImageBoxes', 'setShowAnswer']),

    onSubmit: function() {
      const self=this;
      const total_num = self.$store.getters.getImageBoxes.length

      
      const ansProposed = ['event_content-title', 'event_content-title',
      'event_location-online', 'event_datetime-main_date', 'event_datetime-main_date', 'event_datetime-main_date', 'event_datetime-main_time', 'event_location-online',
      'host_or_sponsor-brand', 'host_or_sponsor-brand', 'host_or_sponsor-brand',
      'participant-instructions', 'participant-instructions', 'participant-instructions', 'participant-instructions', 'participant-instructions', 'participant-instructions',
      'participant-instructions', 'contact_or_fmi-website', 'contact_or_fmi-website']
      /*
      const ansBaseline = ['list-number', 'list-name', 'list-name', 'list-name', 'list-price',
      'list-number', 'list-name', 'list-name', 'list-name', 'list-price',
      'price-subtotal', 'price-subtotal', 'price-tax', 'price-tax',
      'price-total', 'price-total', 'payment-cash', 'payment-cash',
      'payment-change', 'payment-change', 'payment-change']
      */
      
      var boxes = self.$store.getters.getImageBoxes
      for (var box in boxes) {
        var newgt = {}
        var tempbox = boxes[box]
        //var gt = tempbox.gtlabel.cat + '-' + tempbox.gtlabel.subcat
        var gt = ansProposed[box]
        //console.log(tempbox.box_id, tempbox.text, ":", tempbox.label, "vs.", gt)
        if (tempbox.label !== gt) {
          tempbox.correct = false
        } else {
          tempbox.correct = true
        }
        tempbox.anschecked = true

        newgt['cat'] = gt.split('-')[0]
        newgt['subcat'] = gt.split('-')[1]
        tempbox.gtlabel = newgt
      }

      
      var accuracy = (boxes.filter(v => v.correct).length / total_num * 1.00 * 100).toFixed(2)
      var wrong = total_num - boxes.filter(v => v.correct).length
      if (wrong > 0) {
        alert("You are " + accuracy + "% correct. Please check the answers to the " + wrong + " boxes that you incorrectly labeled on the image.")
      }
      else {
        alert("You got everything correct! Please move on to the actual task. Good job!! 😊")
      }
      
      self.setShowAnswer(true/*!this.$store.getters.getShowAnswer*/)
      const new_boxes = [...boxes]
      self.updateImageBoxes(new_boxes)
      
      
    }
  },

  computed: {
    
    disabled() {
      const total_num = this.$store.getters.getImageBoxes.length
      return this.$store.getters.getAnnotatedBoxes.map(v => v.boxes).flat(1).length < total_num
    }
    
  }
}
</script>
