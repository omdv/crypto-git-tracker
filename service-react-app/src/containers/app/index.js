import React from 'react';
import { Route, Link } from 'react-router-dom'
import Home from '../home'
import About from '../about'
import Footer from '../../components/Footer'
import './index.css'


    // <header>
    //   <Link to="/">Home</Link>
    //   <Link to="/about-us">About</Link>
    // </header>

const App = () => (
  <div>
    <main>
      <Route exact path="/" component={Home} />
      <Route exact path="/about-us" component={About} />
    </main>
    <Footer />
  </div>
)

export default App