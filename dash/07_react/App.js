/* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';

import { ExampleComponent, TextInput, TextInputParentState } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            value: 'Состояние родителя'
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
            <div>
                <h1>Hello, Dash!</h1>
                {/* <ExampleComponent
                    setProps={this.setProps}
                    {...this.state}
                /> */}
                <TextInput label="Input с собственным состоянием" />
                <br />
                <TextInputParentState
                    label="Input с родительским состоянием"
                    value={this.state.value}
                    setProps={this.setProps}
                />
            </div>
        )
    }
}

export default App;
