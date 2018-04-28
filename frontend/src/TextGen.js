import React, { Component } from 'react';
import { Button } from 'react-bootstrap';
import './styles/TextGen.css';
import loader from './images/tail-spin.svg';

const API_URL = 'https://paska-api.herokuapp.com/random_text'
const COLORS = ['#ff9edd', '#9ee0e5', '#a2e8a6', '#e8e071', '#ea9a6b', '#a397ef']


class TextGen extends Component {

  constructor(props) {
    super(props);
    this.state = { text: '', loading: true, number: null };
  }


  fetchData() {
    var that = this;
    let number = Math.floor(Math.random() * 999)
    that.setState({ number: number, loading: true });
    fetch(API_URL)
    .then(function(response) {
      if (response.status >= 400) {
        throw new Error("Bad response from server");
      }
      return response.json();
    })
    .then(function(data) {
      that.setState({ text: data.data, loading: false });
    });
  }


  componentDidMount() {
    this.fetchData()
  }


  getRandomColor() {
    let color = COLORS[Math.floor(Math.random()*COLORS.length)];
    console.log(color)
    return color
  }


  renderContent() {
    if (this.state.loading) {
      return (
        <img src={loader} alt={loader}/>
      )
    } else return (
      <div className="generated-text">
        <h3 style={{'color': this.getRandomColor()}}>{'"' + this.state.text + '"'}</h3>
        <Button className="button" bsStyle="primary" onClick={this.fetchData.bind(this)}>Go deeper</Button>
      </div>
    )
  }


  render() {
    return (
      <div className="content">
        <h2> Deep quote #{this.state.number}</h2>
        {this.renderContent()}
      </div>
    );
  }
}

export default TextGen;
