// Form.jsx
import React, { useState } from 'react';
import { calculateSum } from './Utils';

export function Form() {
    const [inputA, setInputA] = useState('');
    const [inputB, setInputB] = useState('');
    const [sum, setSum] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        const result = calculateSum(Number(inputA), Number(inputB));
        setSum(result);
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Input A:
                    <input
                        type="number"
                        value={inputA}
                        onChange={(e) => setInputA(e.target.value)}
                    />
                </label>
                <label>
                    Input B:
                    <input
                        type="number"
                        value={inputB}
                        onChange={(e) => setInputB(e.target.value)}
                    />
                </label>
                <button type="submit">Calculate Sum</button>
            </form>
            {sum !== null && <p>The sum is: {sum}</p>}
        </div>
    );
}
