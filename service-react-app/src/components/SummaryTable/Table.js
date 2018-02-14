import React, { Component } from 'react'
import { Sparklines, SparklinesLine } from 'react-sparklines'
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import './Table.css'

var numeral = require('numeral')

class SummaryTable extends Component {
  constructor(props){
    super(props);
    this.state = { selected: new Set([]) };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange = (index) => {
    let { selected } = this.state
    selected.has(index) ? selected.delete(index) : selected.add(index)
    this.setState({selected: selected})
  }

  render() {
    return (
    <div className="Wrapper">
      <ReactTable
        data={this.props.data}
        columns={this.props.columns}
        loading={this.props.loading}
        showPagination={true}
        defaultPageSize={10}
        showPageSizeOptions={false}
        minRows={3}
        filterable={false}
        getTrProps={(state, rowInfo) => {
          return {
            onClick: (e) => this.handleChange(rowInfo.index),
            style: {
              background: rowInfo && (this.state.selected.has(rowInfo.index) ? '#00afec' : 'white'),
              color: rowInfo && (this.state.selected.has(rowInfo.index) ? 'white' : 'black')
            }
          }
        }}
        defaultSorted={this.props.sorting} />
    </div>
    )
  }
}

export default SummaryTable
