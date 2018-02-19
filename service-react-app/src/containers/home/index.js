import React, { Component } from 'react'
import { push } from 'react-router-redux'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import axios from 'axios'
import {
  increment,
  incrementAsync,
  decrement,
  decrementAsync
} from '../../modules/counter'

// Charts
import TimeSeriesChart from '../../components/TimeSeriesChart/chart'
import ScatterChart from '../../components/ScatterChart/chart'

// React table
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import {main_table_columns, main_table_sorting} from '../../definitions/main_table'

// Home container styles
import './index.css'

// underscore
// var _ = require('underscore')


// constants
const SPARKLINE_DAYS = 52
const MAX_SELECTED_COINS = 5
const MARGINS = {top: 20, right: 30, bottom: 60, left: 60}

// const Home = props => (
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
  }
  
  componentDidMount() {
    this.getAndPrepareData()
    // select two coins for illustration
    // this.handleChange(2)
    // this.handleChange(3)
  }

  initGraphs() {
    this.handleChange(2)
    this.handleChange(3)
  }

  handleChange(idx) {
    const { summary_table_data, selected_coins } = this.state
    const { commits_data, devs_data } = this.state

    if (selected_coins.has(idx)) {
      selected_coins.delete(idx)
    } else if (selected_coins.size < MAX_SELECTED_COINS) {
      // TODO: show warning
      selected_coins.add(idx)
    }

    let coins = Array.from(selected_coins).map(e => summary_table_data[e].ticker)
    
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
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_commits`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_devs`),
    ])
    .then(axios.spread((r_summary, r_commits, r_devs) => {
      // process data
      let summary = r_summary.data
      let commits = r_commits.data
      let devs = r_devs.data
      
      // convert to date
      commits = this.convertToDate(commits)
      devs = this.convertToDate(devs)
      
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

      // merge contributors with ratio
      summary.map(d => {
        return d['developers']=`${d.unique_contributors} (${d.developers_ratio.toFixed(2)}% > 5)`
      })

      // export variables
      this.setState(
        { summary_table_data: summary,
          summary_table_data_loading: false,
          commits_data: commits,
          commits_data_loading: true,
          devs_data: devs,
          devs_data_loading: true
         }, this.initGraphs)
    }))
    .catch((err) => { console.log(err); })
  }

  render () {
    const { selected_commits, selected_devs } = this.state
    const { summary_table_data, summary_table_data_loading } = this.state
    return (
      <div className="container">
        <div className="col-md-12">
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
              onClick: (e) => this.handleChange(rowInfo.index),
              style: {
                background: rowInfo && (this.state.selected_coins.has(rowInfo.index) ? '#00afec' : 'white'),
                color: rowInfo && (this.state.selected_coins.has(rowInfo.index) ? 'white' : 'black')
              }
            }
          }}
          defaultSorted={main_table_sorting} />
        </div>
        <div className="row">
          <div className="col-md-6">
            <TimeSeriesChart
              data={selected_commits}
              width={400}
              height={300}
              hover_enabled={true}
              legend_enabled={true}
              xAccessor={'date'}
              margins={ MARGINS }
              yLabel={'Commits/week'} />
          </div>
          <div className="col-md-6">
            <TimeSeriesChart
              data={selected_devs}
              width={400}
              height={300}
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
              xLabel={'Commits/week'}
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
              xLabel={'Developers/week'}
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


// <h1>Home</h1>
// <p>Count3: {this.props.count}</p>

// <p>
//   <button onClick={this.props.increment} disabled={this.props.isIncrementing}>Increment</button>
//   <button onClick={this.props.incrementAsync} disabled={this.props.isIncrementing}>Increment Async</button>
// </p>

// <p>
//   <button onClick={this.props.decrement} disabled={this.props.isDecrementing}>Decrementing</button>
//   <button onClick={this.props.decrementAsync} disabled={this.props.isDecrementing}>Decrement Async</button>
// </p>

// <p><button onClick={() => this.props.changePage()}>Go to about page via redux</button></p>

const mapStateToProps = state => ({
  count: state.counter.count,
  isIncrementing: state.counter.isIncrementing,
  isDecrementing: state.counter.isDecrementing
})

const mapDispatchToProps = dispatch => bindActionCreators({
  increment,
  incrementAsync,
  decrement,
  decrementAsync,
  changePage: () => push('/about-us')
}, dispatch)

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Home)