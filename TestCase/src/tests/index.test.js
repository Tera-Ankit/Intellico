
import React from 'react';
import { render } from '@testing-library/react';
import { index } from '../index';

describe('index', () => {
  it('renders correctly', () => {
    expect(index).toBeDefined();
    render(<index />);
  });
});
