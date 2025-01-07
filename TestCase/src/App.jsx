import React from 'react';
import { Form } from './components/Form';
import TodoList from './components/TodoList';

export function App() {
    return (
        <div>
            <h1>My Complex React Application</h1>
            <Form />
            <TodoList />
        </div>
    );
}