
import React from 'react';
import { render } from '@testing-library/react';
import Utils from '../components/Utils';

describe('Utils', () => {
  it('renders correctly', () => {
    expect(Utils).toBeDefined();
    render(<Utils />);
  });
});
