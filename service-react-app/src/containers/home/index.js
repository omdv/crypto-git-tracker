import React, { Component } from 'react'
import axios from 'axios'

// Charts
import TimeSeriesChart from '../../components/TimeSeriesChart/chart'
import ScatterChart from '../../components/ScatterChart/chart'

// React table
import ReactTable from 'react-table/lib/index'
import 'react-table/react-table.css'
import {main_table_columns, main_table_sorting} from '../../definitions/main_table'

// Activity indicators
import ActivityIndicators from '../../components/ActivityIndicators'

// Home container styles
import './index.css'

// constants
const SPARKLINE_DAYS = 52
const MAX_SELECTED_COINS = 5
const MARGINS = {top: 20, right: 30, bottom: 60, left: 60}

class Home extends Component {
  constructor() {
    super()
    this.state = {
      commits_data: [],
      commits_data_loading: true,
      devs_data: [],
      devs_data_loading: true,
      summary_table_data: [],
      summary_table_data_loading: true,
      activity_data: [],
      activity_data_loading: true,
      selected_coins: new Set([]),
      selected_commits: [
        {'date': new Date(2009, 8, 29)},
        {'date': new Date()}
      ],
      selected_devs: [
        {'date': new Date(2009, 8, 29)},
        {'date': new Date()}
      ],
    }
    this.resetCoins = this.resetCoins.bind(this)
  }
  
  componentDidMount() {
    this.getAndPrepareData()
  }

  // choose "BTC" and "BCH" for initial graph
  initGraphs() {
    this.handleChange("BTC")
    this.handleChange("BCH")
  }

  resetCoins = () => {
    this.setState({selected_coins: new Set(["BTC"])},
    () => this.handleChange("BTC"))
  }

  handleChange(idx) {
    const { summary_table_data, selected_coins } = this.state
    const { commits_data, devs_data } = this.state

    if (selected_coins.has(idx)) {
      selected_coins.delete(idx)
    } else if (selected_coins.size < MAX_SELECTED_COINS) {
      selected_coins.add(idx)
    }

    let coins = Array.from(selected_coins)
    
    // select commits
    if (commits_data.length > 0) {
      let selected_commits = commits_data.map(x => {
        let _o = {date: x.date}
        for (var _e in coins){
          _o[coins[_e]] = x[coins[_e]]
        }
        return _o
      })
      this.setState({selected_commits: selected_commits})
    }

    // select developers
    if (devs_data.length > 0) {
      let selected_devs = devs_data.map(x => {
        let _o = {date: x.date}
        for (var _e in coins){
          _o[coins[_e]] = x[coins[_e]]
        }
        return _o
      })
      this.setState({selected_devs: selected_devs})
    }

    // add indicator to summary_table_data that coins are selected
    summary_table_data.map((d,i) => {
      if (selected_coins.has(d["ticker"])) {
        d.selected = 1
      } else {
        d.selected = 0
      }
      return d
    })

    // update selected coins
    this.setState({selected_coins: selected_coins})
  }

  convertToDate(arr) {
    return arr.map((d,i) => {
      d.date = new Date(d.date)
      return d
    })
  }

  getAndPrepareData() {
    axios.all([
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/summary_table`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/commits`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/developers`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/activity_levels`)
    ])
    .then(axios.spread((r_summary, r_commits, r_devs, r_activity) => {
      // process data
      let summary = r_summary.data
      let commits = r_commits.data
      let devs = r_devs.data
      let activity = r_activity.data
      
      // convert to date
      commits = this.convertToDate(commits)
      devs = this.convertToDate(devs)
      activity.map((d,i) => {
        d.max_commits_date = new Date(d.max_commits_date)
        d.max_devs_date = new Date(d.max_devs_date)
        return d
      })
      
      // create sparklines for commits
      let _s_commits = commits.slice(commits.length - SPARKLINE_DAYS)
      summary.map((d,i) => {
        return d['sparkline_commits'] = _s_commits.map(s => s[d.ticker])
      })

      // create sparklines for devs
      let _s_devs = devs.slice(devs.length - SPARKLINE_DAYS)
      summary.map((d,i) => {
        return d['sparkline_devs'] = _s_devs.map(s => s[d.ticker])
      })

      // sum of commits
      // summary_table_data.ma

      // export variables
      this.setState({ activity_data: activity, activity_data_loading: false})

      // export variables
      this.setState(
        { summary_table_data: summary,
          summary_table_data_loading: false,
          commits_data: commits,
          commits_data_loading: true,
          devs_data: devs,
          devs_data_loading: true,
         }, this.initGraphs)
    }))
    .catch((err) => { console.log(err); })
  }

  render () {
    const { selected_commits, selected_devs } = this.state
    const { summary_table_data, summary_table_data_loading } = this.state
    return (
      <div className="container">
          { !this.state.activity_data_loading && 
            <ActivityIndicators activity={this.state.activity_data[0]}/> }
        <div className="col-md-12">
          <div style={{"textAlign": "right"}}>
            <p className="note">{"Tracking " + summary_table_data.length + " projects, " +
            summary_table_data.reduce((s,e) => s+e["number_of_commits"], 0) + " commits, " +
            summary_table_data.reduce((s,e) => s+e["repos"].split(",").length , 0) + " repos"}</p>
          </div>
          <ReactTable
          data={summary_table_data}
          columns={main_table_columns}
          loading={summary_table_data_loading}
          showPagination={true}
          defaultPageSize={10}
          showPageSizeOptions={false}
          minRows={3}
          filterable={false}
          getTrProps={(state, rowInfo) => {
            return {
              onClick: (e) => this.handleChange(rowInfo.original.ticker),
              style: {
                background: rowInfo && (this.state.selected_coins.has(rowInfo.original.ticker) ? '#00afec' : 'white'),
                color: rowInfo && (this.state.selected_coins.has(rowInfo.original.ticker) ? 'white' : 'black')
              }
            }
          }}
          defaultSorted={main_table_sorting} />
          <div style={{"textAlign": "right"}}>
            <p>Selected {this.state.selected_coins.size} of {MAX_SELECTED_COINS}.&nbsp;
              <span className="button" onClick={this.resetCoins}>Reset</span>
            </p>
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            <TimeSeriesChart
              data={selected_commits}
              width={250}
              height={250}
              hover_enabled={true}
              legend_enabled={true}
              xAccessor={'date'}
              margins={ MARGINS }
              yLabel={'Commits/week'} />
          </div>
          <div className="col-md-6">
            <TimeSeriesChart
              data={selected_devs}
              width={250}
              height={250}
              hover_enabled={true}
              legend_enabled={true}
              xAccessor={'date'}
              margins={ MARGINS }
              yLabel={'Developers/week'} />
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            {!summary_table_data_loading && <ScatterChart
              data = {summary_table_data}
              xAccessor={'mean_commits_period'}
              yAccessor={'market_cap'}
              outlierAccessorPos={'commits_ratio_90'}
              outlierAccessorNeg={'commits_ratio_10'}
              xLabel={'Commits per week'}
              yLabel={'Market Cap $M'}
              width={250}
              height={250}
              margins={ MARGINS } />}
          </div>
          <div className="col-md-6">
            {!summary_table_data_loading && <ScatterChart
              data = {summary_table_data}
              xAccessor={'mean_devs_period'}
              yAccessor={'market_cap'}
              outlierAccessorPos={'devs_ratio_90'}
              outlierAccessorNeg={'devs_ratio_10'}
              xLabel={'Developers per week'}
              yLabel={'Market Cap $M'}
              width={250}
              height={250}
              margins={ MARGINS } />}
          </div>
        </div>
      </div>
    )
  }
}

export default Home