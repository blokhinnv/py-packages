import React, { Component } from 'react'

class TextInput extends Component {
    constructor(props) {
        // props - свойства компонента
        // Они передаются от родительского компонента,
        // вызов super(props) позволяет писать this.props
        super(props);
        this.state = {
            "value": "default"
        }
    }

    handleInputChange = (e) => {
        // новое значение со страницы
        const newValue = e.target.value;
        // обновить поле state
        // этот метод наследуется от Component:
        // обновляет state и перерисовывает компонент
        this.setState({
            value: newValue
        })
    }

    render() {
        // React вызовет этот метод, когда захочет отрисовать этот компонент
        // мы можем вернуть обычную строку или JSX
        // {} позволяют писать внутри обычный JS код
        return (
            <div>
                <p>{this.props.label}</p>
                <input value={this.state.value} onChange={this.handleInputChange} />
                <p>Value компонента: {this.state.value}</p>
            </div>
        )
    }
}

export default TextInput;
