import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import InformedConsent from '../views/InformedConsent.vue'
import Instruction from '../views/Instruction.vue'
import Practice from '../views/Practice.vue'
import DeferredAnnotation from '../views/Annotation.vue'
import PageNotFound from '../views/404.vue'
import AnnotDone from '../views/AnnotDone.vue'
import Review from '../views/Review.vue'
import ReviewSuggestion from '../views/ReviewSuggestion.vue'
import PostSurvey from '../views/PostSurvey.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/annotation/:docType/',
    name: 'DeferredAnnotation',
    component: DeferredAnnotation
  },
  {
    path: '/landing',
    name: 'Landing',
    component: Landing,
    alias: '/'
  },
  {
    path: '/informed-consent',
    name: 'InformedConsent',
    component: InformedConsent
  },
  {
    path: '/instruction/:docType/',
    name: 'Instruction',
    component: Instruction
  },
  {
    path: '/practice/:docType/',
    name: 'Practice',
    component: Practice
  },
  {
    path: '/annot-done/:docType/',
    name: 'AnnotDone',
    component: AnnotDone
  },
  {
    path: '/review/:docType/',
    name: 'Review',
    component: Review
  },

  {
    path: '/review-suggestion/:docType/',
    name: 'ReviewSuggestion',
    component: ReviewSuggestion
  },  
  {
    path: '/postsurvey/',
    name: 'PostSurvey',
    component: PostSurvey
  },

  {
    path: "*",
    name: '404',
    component: PageNotFound
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
