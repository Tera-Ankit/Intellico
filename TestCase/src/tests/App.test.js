
import React from 'react';
import { render } from '@testing-library/react';
import { App } from '../App';

describe('App', () => {
  it('renders correctly', () => {
    expect(App).toBeDefined();
    render(<App />);
  });
});
