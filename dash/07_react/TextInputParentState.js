import React, { Component } from 'react'

class TextInputParentState extends Component {
    constructor(props) {
        // props - свойства компонента
        // Они передаются от родительского компонента,
        // вызов super(props) позволяет писать this.props
        super(props);
    }

    handleInputChange = (e) => {
        // новое значение со страницы
        const newValue = e.target.value;
        // обновить поле state
        // этот метод наследуется от Component:
        // обновляет state и перерисовывает компонент
        this.props.setProps({
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
                {/* заменяем this.state на this.props */}
                <input value={this.props.value} onChange={this.handleInputChange} />
                <p>Value родителя: {this.props.value}</p>
            </div>
        )
    }
}

export default TextInputParentState;
