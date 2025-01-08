
import React from 'react';
import { render } from '@testing-library/react';
import { Form } from '../components/Form';

describe('Form', () => {
  it('renders correctly', () => {
    expect(Form).toBeDefined();
    render(<Form />);
  });
});
