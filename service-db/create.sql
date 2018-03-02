CREATE DATABASE analytics_prod;
CREATE DATABASE analytics_dev;
CREATE DATABASE analytics_test;

CREATE TABLE IF NOT EXISTS control_repos
(
  id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  ticker CHARACTER VARYING(16) NOT NULL,
  apihandle CHARACTER VARYING(64) NOT NULL,
  url CHARACTER VARYING(128) NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS commits
(
  id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  login CHARACTER VARYING(64),
  message TEXT,
  repo CHARACTER VARYING(64) NOT NULL,
  ticker CHARACTER VARYING(16) NOT NULL,
  apihandle CHARACTER VARYING(64) NOT NULL,
  url CHARACTER VARYING(256) NOT NULL,
  "date" TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS git_rate_limit
(
  id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "time" TIMESTAMP NOT NULL,
  rate INTEGER NOT NULL
);