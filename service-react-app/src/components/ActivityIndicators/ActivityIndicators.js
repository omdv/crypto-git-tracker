import React from 'react'
import './ActivityIndicators.css'

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

const ActivityIndicators = (props) => {
	const commits_start = props.activity.max_commits_date
	let commits_end = addDays(commits_start, 7)

	const devs_start = props.activity.max_devs_date
	let devs_end = addDays(devs_start, 7)

      return <div className="row">
      <div className="col-md-3">
        <div className="row">
          <p className="activity-label">Commits activity now</p>
        </div>
        <div className="row">
          <p className="activity-levels">{props.activity.current_commits_level.toFixed(0)}%</p>
        </div>
      </div>
      <div className="col-md-3">
  			<div className="row">
  				<p className="activity-label">Most commits on</p>
  			</div>
  			<div className="row">
  				<p className="activity-dates">{commits_start.toLocaleDateString('en-GB',
	      			{'day':'numeric', 'month':'short', 'year':'numeric'})} - {(commits_end).toLocaleDateString('en-GB',
	      			{'day':'numeric', 'month':'short', 'year':'numeric'})}
  				</p>
  			</div>
  		</div>
  		<div className="col-md-3">
  			<div className="row">
  				<p className="activity-label">Most developers on</p>
  			</div>
  			<div className="row">
  				<p className="activity-dates">{devs_start.toLocaleDateString('en-GB',
	      			{'day':'numeric', 'month':'short', 'year':'numeric'})} - {(devs_end).toLocaleDateString('en-GB',
	      			{'day':'numeric', 'month':'short', 'year':'numeric'})}
  				</p>
  			</div>
  		</div>
  		<div className="col-md-3">
  			<div className="row">
  				<p className="activity-label">Developers activity now</p>
  			</div>
  			<div className="row">
  				<p className="activity-levels">{props.activity.current_devs_level.toFixed(0)}%</p>
  			</div>
  		</div>

    </div>
}

export default ActivityIndicators