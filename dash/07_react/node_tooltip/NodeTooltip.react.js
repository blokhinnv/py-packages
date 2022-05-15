import React, { useState, Component } from "react";
import PropTypes, { string } from 'prop-types';

class NodeTooltip extends Component {
    constructor(props) {
        super(props)
    }

    static defaultProps = {
        visible: true,
        offsetX: 0,
        offsetY: 0,
        top: 0,
        left: 0,
        lastNodeTop: 0,
        lastNodeLeft: 0,
        maxDistance: 50,
    };

    state = {
        xPosition: 0,
        yPosition: 0,
        mouseMoved: false,
        listenerActive: false,
    };

    componentDidMount() {
        this.addListener();
    }

    componentDidUpdate() {
        this.updateListener();
    }

    componentWillUnmount() {
        this.removeListener();
    }

    getTooltipPosition = ({ clientX: xPosition, clientY: yPosition }) => {
        this.setState({
            xPosition,
            yPosition,
            mouseMoved: true,
        });

        if (this.props.lastNodeTop !== null) {
            const distance = Math.pow(
                Math.pow(this.state.yPosition - this.props.lastNodeTop, 2) +
                Math.pow(this.state.xPosition - this.props.lastNodeLeft, 2),
                0.5
            );

            this.props.setProps({
                top: this.state.yPosition,
                left: this.state.xPosition,
                visible: distance <= this.props.maxDistance
            })
        }
        else {
            console.log("!");
            this.props.setProps({
                top: this.state.yPosition,
                left: this.state.xPosition
            })
        }
    };

    addListener = () => {
        window.addEventListener('mousemove', this.getTooltipPosition);
        this.setState({ listenerActive: true });
    };

    removeListener = () => {
        window.removeEventListener('mousemove', this.getTooltipPosition);
        this.setState({ listenerActive: false });
    };

    updateListener = () => {
        if (!this.state.listenerActive && this.props.visible) {
            this.addListener();
        }

        if (this.state.listenerActive && !this.props.visible) {
            this.removeListener();
        }
    };

    render() {
        return (
            <div
                id={this.props.id}
                className={this.props.className}
                style={{
                    display: this.props.visible && this.state.mouseMoved ? 'block' : 'none',
                    position: 'fixed',
                    top: this.state.yPosition + this.props.offsetY,
                    left: this.state.xPosition + this.props.offsetX,
                    ...this.props.style,
                }}
            >
                {this.props.children}
            </div>
        );
    }
}

NodeTooltip.propTypes = {
    id: PropTypes.string,
    children: PropTypes.node,
    visible: PropTypes.bool,
    offsetX: PropTypes.number,
    offsetY: PropTypes.number,
    lastNodeTop: PropTypes.number,
    lastNodeLeft: PropTypes.number,
    top: PropTypes.number,
    left: PropTypes.number,
    maxDistance: PropTypes.number,
    className: PropTypes.string,
    style: PropTypes.object, // eslint-disable-line react/forbid-prop-types
};

export default NodeTooltip;
