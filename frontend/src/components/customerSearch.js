import React from "react";
import TextField from '@material-ui/core/TextField';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import '../css/common.css';


const useStyles = makeStyles((theme) => ({
  submit: {
    margin: theme.spacing(3, 0, 2),
  }
  }));

let searchInput = {'first_name': '', 'last_name': '', 'phone': ''};

const handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        searchInput[name] = value;
};

function SearchPage(props) {
  return (
  <Container component="main" maxWidth="xs">
   <form className={useStyles.form} noValidate>
    <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            name="first_name"
            label="First Name"
            type="text"
            id="first_name"
            onChange={handle_change}
          />
    <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            name="last_name"
            label="Last Name"
            type="text"
            id="last_name"
            onChange={handle_change}
          />
    <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            name="phone"
            label="Phone"
            type="number"
            id="phone"
            onInput = {(e) => {
                 e.target.value.length > 0 ? e.target.value = Math.max(0, parseInt(e.target.value) ).toString().slice(0,10) : e.target.value = ''
            }}
            onChange={handle_change}
          />
    <Button
            fullWidth
            variant="contained"
            color="primary"
            className={useStyles.submit}
            onClick={e => props.handle_option_click(e, 'listcustomer', searchInput)}
          >
            Submit
    </Button>
    </form>
  </Container>
  );
}

export default SearchPage;
