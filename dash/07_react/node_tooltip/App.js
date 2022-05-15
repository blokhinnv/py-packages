/* eslint no-magic-numbers: 0 */
import React, { useState } from 'react';

import { NiceInput, NodeTooltip } from '../lib';

const App = function (props) {
    const [inputState, setInputState] = useState({
        value: 'Some value...'
    })
    return (
        <div>
            <NiceInput
                id="some_id"
                label="Input label!1"
                value={inputState.value}
                // setProps={e => setInputState({ ...inputState, value: e })}
                setProps={setInputState}
            />
            <NodeTooltip
                id="my_tooltip1"
                visible={true}
                offsetX={15}
                offsetY={15}
            >
                <span>Текст</span>
            </NodeTooltip>
        </div>
    )
}

export default App;
