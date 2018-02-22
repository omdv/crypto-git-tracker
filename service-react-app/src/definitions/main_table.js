import React from 'react'
import { Sparklines, SparklinesLine } from 'react-sparklines'
var numeral = require('numeral')

export let main_table_columns = [{
    Header: 'Coin',
    Cell: ({ row, original }) => <a href={"https://coinmarketcap.com/currencies/"+original.apihandle}>{original.name}</a>,
    minWidth: 80
  }, {
    Header: 'Market Cap $M',
    accessor: 'market_cap',
    Cell: props => <p>{numeral(props.value).format('$ 0,0').toUpperCase()}</p>
  }, {
    Header: 'Price',
    accessor: 'price',
    Cell: props => <p>{numeral(props.value).format('$0,0.00').toUpperCase()}</p>,
    maxWidth: 90
  }, {
    Header: 'Age, days',
    accessor: 'days_since_launch',
    maxWidth: 70
  }, {
    Header: 'Commits',
    accessor: 'number_of_commits',
    maxWidth: 70
  }, {
    Header: 'Avg/week',
    accessor: 'mean_commits_period',
    Cell: props => <p>{props.value.toFixed(2)}</p>,
    maxWidth: 70
  }, { 
    Header: '../market',
    accessor: 'avg_commits_per_market_cap',
    Cell: props => <p>{props.value.toFixed(2)}</p>,
    maxWidth: 70
  }, {
    Header: 'Trend',
    accessor: 'sparkline_commits',
    Cell: props => <Sparklines data={props.value} height={24} margin={0}>
      <SparklinesLine color="blue" /></Sparklines>,
    sortable: false,
    minWidth: 100
  }, {
    Header: 'Devs',
    accessor: 'unique_contributors',
    maxWidth: 50
  }, {
    Header: '% > 5',
    accessor: 'developers_ratio',
    Cell: props => <p>{props.value.toFixed(2)}</p>,
    minWidth: 50
  }, {
    Header: 'Avg/week',
    accessor: 'mean_devs_period',
    Cell: props => <p>{props.value.toFixed(2)}</p>,
    maxWidth: 70
  }, {
    Header: '../market',
    accessor: 'avg_devs_per_market_cap',
    Cell: props => <p>{props.value.toFixed(2)}</p>,
    maxWidth: 70
  }, {
    Header: 'Trend',
    accessor: 'sparkline_devs',
    Cell: props => <Sparklines data={props.value} height={24} margin={0}>
      <SparklinesLine color="blue" /></Sparklines>,
    sortable: false,
    minWidth: 100
  }, {
    Header: 'Repos',
    accessor: 'repos',
    Cell: props =><p>{props.value.split(',').map((v,i) =>
        <a href={'https://github.com/'+v} key={i}>[{i+1}]</a>)}</p>,
    minWidth: 60,
    sortable: false
  }]

export let main_table_sorting = [{
    id: "market_cap",
    desc: true
}]