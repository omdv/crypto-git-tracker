import React, { Component } from 'react'
import { Sparklines, SparklinesLine } from 'react-sparklines'
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import './Table.css'


class SummaryTable extends Component {
  constructor() {
    super()
  }

  columns = [{
      Header: 'Coin',
      accessor: 'coin'
    }, {
      Header: 'Commits',
      accessor: 'number_of_commits'
    }, {
      Header: 'Developers',
      accessor: 'developers'
    }, {
      Header: 'Daily commits',
      accessor: 'daily_commits',
    }, {
      Header: 'Commits history',
      accessor: 'sparkline',
      Cell: props => <Sparklines data={props.value} height={24} margin={0}>
        <SparklinesLine color="blue" /></Sparklines>
    }, {
      Header: 'Last month MVP',
      accessor: 'monthly_mvp',
      Cell: props => <a href={"https://github.com/"+props.value}>{props.value}</a>
    }]

  render() {
    return (
    <div className="Wrapper">
      <ReactTable
        data={this.props.data}
        columns={this.columns}
        loading={this.props.loading}
        showPagination={false}
        showPageSizeOptions={false}
        minRows={3}
        filterable={false} />
    </div>
    )
  }
}

export default SummaryTable
