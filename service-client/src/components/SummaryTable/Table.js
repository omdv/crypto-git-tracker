import React, { Component } from 'react'
import { Sparklines, SparklinesLine } from 'react-sparklines'
import {Tooltip} from 'react-lightweight-tooltip'
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import './Table.css'

var numeral = require('numeral')

class SummaryTable extends Component {

  tooltipStyle = {
    content: {
      backgroundColor: 'white',
      color: '#000',
      border: 'solid black 0.1px',
      borderRadius: 4,
      bottom: '0%'
    },
    tooltip: {
      backgroundColor: 'white',
      zIndex: 999,
      position: 'relative',
      margin: '0px',
      padding: '0px'
    },
    arrow: {
      borderTop: 'solid white .1px',
    },
    gap: {
      position: 'absolute',
      width: '100%',
      height: '0px',
      bottom: '-0px',
    }
  }

  columns = [{
      Header: 'Coin',
      Cell: ({ row, original }) => <a href={"https://coinmarketcap.com/currencies/"+original.apihandle}>{original.name}</a>,
      minWidth: 70
    }, {
      Header: 'Market Cap',
      accessor: 'market_cap',
      Cell: props => <p>{numeral(props.value).format('$ 0.000 a').toUpperCase()}</p>
    }, {
      Header: 'Price',
      accessor: 'price',
      Cell: props => <p>{numeral(props.value).format('$0,0.00').toUpperCase()}</p>
    }, {
      Header: 'Repos',
      accessor: 'repos',
      Cell: props => <Tooltip
        styles={this.tooltipStyle}
        content={props.value.split(',').map((v,i) =>
          <a href={'https://github.com/'+v} key={i}>[{i}]</a>)}>
          {props.value.split(',').length}
        </Tooltip>,
      minWidth: 70
    }, {
      Header: 'Commits',
      accessor: 'number_of_commits'
    }, {
      Header: 'Commits today',
      accessor: 'today_commits_merged',
    }, {
      Header: 'Daily commits',
      accessor: 'sparkline_commits',
      Cell: props => <Sparklines data={props.value} height={24} margin={0}>
        <SparklinesLine color="blue" /></Sparklines>
    }, {
      Header: 'Developers',
      accessor: 'developers'
    }, {
      Header: 'Devs today',
      accessor: 'today_devs_merged',
    }, {
      Header: 'Daily devs',
      accessor: 'sparkline_devs',
      Cell: props => <Sparklines data={props.value} height={24} margin={0}>
        <SparklinesLine color="blue" /></Sparklines>
    }, {
      Header: 'Last month MVP',
      accessor: 'monthly_mvp',
      Cell: props => <a href={"https://github.com/"+props.value}>{props.value}</a>
    }]

  sorting = [{
      id: "market_cap",
      desc: true
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
        filterable={false}
        defaultSorted={this.sorting} />
    </div>
    )
  }
}

export default SummaryTable
