
import React from 'react';
import { render } from '@testing-library/react';
import TodoList from '../components/TodoList';

describe('TodoList', () => {
  it('renders correctly', () => {
    expect(TodoList).toBeDefined();
    render(<TodoList />);
  });
});
