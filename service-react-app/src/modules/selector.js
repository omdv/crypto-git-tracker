export const REQUEST_UPDATE = 'selector/REQUEST_UPDATE'
export const UPDATE = 'selector/UPDATE'

const initialState = {
  selection: new Set([]),
  updating: false,
}

export default (state = initialState, action) => {
  switch (action.type) {
    case REQUEST_UPDATE:
      return {
        ...state,
        updating: true
      }

    case UPDATE:
      return {
        ...state,
        selection: action.selection,
        updating: !state.updating
      }

    default:
      return state
  }
}

export const update_selection = () => {
  return dispatch => {
    dispatch({
      type: REQUEST_UPDATE
    })

    dispatch({
      type: UPDATE
    })
  }
}

// export const incrementAsync = () => {
//   return dispatch => {
//     dispatch({
//       type: INCREMENT_REQUESTED
//     })

//     return setTimeout(() => {
//       dispatch({
//         type: INCREMENT
//       })
//     }, 3000)
//   }
// }