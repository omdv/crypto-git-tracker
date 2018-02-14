import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import counter from './counter'
import selector from './selector'

export default combineReducers({
  routing: routerReducer,
  counter,
  selector
})