import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <form action="categories" method="get" encType="multipart/form-data">
                        Select image to upload:
                        <input type="file" name="fileToUpload" id="fileToUpload"/>
                        <input type="submit" value="Upload Image" name="submit"/>
                    </form>
                </header>
            </div>
        );
    }
}

export default App;
