import React, { Component } from 'react';
import SignIn from './accounts/signIn';
import './App.css';
import Dashboard from './components/dashboard';
import config from 'react-global-configuration';

class App extends Component {
  constructor(props) {
    super(props);
    config.set({ companyTitle: 'LibreHatti' }, { freeze: false, environment: 'test' });
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      username: '',
    };
  }

  verify_login = () => {
    if(localStorage.getItem('token') === null){
       this.setState({
          logged_in: false,
       });
    } else {
        fetch('http://localhost:8000/useraccounts/verify-token/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({'token': localStorage.getItem('token')})
          })
            .then(res => {
                if(res.status !== 200){
                    this.setState({
                    logged_in: false,
                });
            }
            });
     }
  }

  componentDidMount() {

    if (this.state.logged_in) {
      this.verify_login();
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/useraccounts/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.user.username
        });
      });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/core/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  handle_option_click = (e, component, data) =>{
    e.preventDefault();
    this.verify_login();
    this.setState({
        component_toMount: component,
        component_data: data
    });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let ui;
    if(this.state.logged_in){
        ui = <Dashboard state={this.state} handle_option_click={this.handle_option_click} handle_logout={this.handle_logout}/>;
    } else{
            ui = <SignIn handle_login={this.handle_login} />;
    }

    return (
      <div className="App">
        {ui}
      </div>
    );
}
}

export default App;
