import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskForm from './TaskForm';

describe('TaskForm', () => {
  const mockOnCreateTask = jest.fn();

  beforeEach(() => {
    mockOnCreateTask.mockClear();
  });

  it('renders the form elements correctly', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    expect(screen.getByPlaceholderText('Enter a new task...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add task/i })).toBeInTheDocument();
  });

  it('allows user to type in the input field', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    const input = screen.getByPlaceholderText('Enter a new task...');
    fireEvent.change(input, { target: { value: 'Test task' } });

    expect(input).toHaveValue('Test task');
  });

  it('calls onCreateTask with the input value when submitted', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    const input = screen.getByPlaceholderText('Enter a new task...');
    fireEvent.change(input, { target: { value: 'Test task' } });

    const button = screen.getByRole('button', { name: /add task/i });
    fireEvent.click(button);

    expect(mockOnCreateTask).toHaveBeenCalledWith('Test task');
    expect(input).toHaveValue('');
  });

  it('shows error when submitted with empty input', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    const input = screen.getByPlaceholderText('Enter a new task...');
    fireEvent.change(input, { target: { value: '' } });

    const button = screen.getByRole('button', { name: /add task/i });
    fireEvent.click(button);

    expect(screen.getByText('Task title cannot be empty')).toBeInTheDocument();
    expect(mockOnCreateTask).not.toHaveBeenCalled();
  });

  it('clears error when user starts typing after error', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    // Trigger error first
    const input = screen.getByPlaceholderText('Enter a new task...');
    const button = screen.getByRole('button', { name: /add task/i });

    fireEvent.click(button);
    expect(screen.getByText('Task title cannot be empty')).toBeInTheDocument();

    // Now type something
    fireEvent.change(input, { target: { value: 'Valid task' } });

    expect(screen.queryByText('Task title cannot be empty')).not.toBeInTheDocument();
  });

  it('disables submit button when input is empty', () => {
    render(<TaskForm onCreateTask={mockOnCreateTask} />);

    const button = screen.getByRole('button', { name: /add task/i });
    expect(button).toBeDisabled();

    const input = screen.getByPlaceholderText('Enter a new task...');
    fireEvent.change(input, { target: { value: 'Valid task' } });

    expect(button).not.toBeDisabled();
  });
});