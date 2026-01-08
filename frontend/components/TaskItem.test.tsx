import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskItem from './TaskItem';
import { Task } from '../types/task';

describe('TaskItem', () => {
  const mockTask: Task = {
    id: 1,
    title: 'Test task',
    completed: false,
  };

  const mockOnUpdateTask = jest.fn();
  const mockOnDeleteTask = jest.fn();
  const mockOnToggleTask = jest.fn();

  beforeEach(() => {
    mockOnUpdateTask.mockClear();
    mockOnDeleteTask.mockClear();
    mockOnToggleTask.mockClear();
  });

  it('renders task title and checkbox', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    expect(screen.getByText('Test task')).toBeInTheDocument();
    expect(screen.getByRole('checkbox')).toBeInTheDocument();
    expect(screen.getByRole('checkbox')).not.toBeChecked();
  });

  it('displays strikethrough for completed tasks', () => {
    const completedTask = { ...mockTask, completed: true };
    render(
      <TaskItem
        task={completedTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    const taskText = screen.getByText('Test task');
    expect(taskText).toHaveClass('line-through');
  });

  it('calls onToggleTask when checkbox is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(mockOnToggleTask).toHaveBeenCalledWith(1);
  });

  it('enters edit mode when task title is double-clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    const taskText = screen.getByText('Test task');
    fireEvent.doubleClick(taskText);

    const input = screen.getByDisplayValue('Test task');
    expect(input).toBeInTheDocument();
  });

  it('calls onUpdateTask when editing is saved', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    // Enter edit mode
    const taskText = screen.getByText('Test task');
    fireEvent.doubleClick(taskText);

    // Change the input value
    const input = screen.getByDisplayValue('Test task');
    fireEvent.change(input, { target: { value: 'Updated task' } });

    // Save by pressing Enter
    fireEvent.keyDown(input, { key: 'Enter' });

    expect(mockOnUpdateTask).toHaveBeenCalledWith(1, { title: 'Updated task' });
  });

  it('shows delete confirmation when delete button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    const deleteButton = screen.getByText('🗑️');
    fireEvent.click(deleteButton);

    expect(screen.getByText('Yes')).toBeInTheDocument();
    expect(screen.getByText('No')).toBeInTheDocument();
  });

  it('calls onDeleteTask when delete is confirmed', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    // Click delete button to show confirmation
    fireEvent.click(screen.getByText('🗑️'));

    // Click Yes to confirm
    fireEvent.click(screen.getByText('Yes'));

    expect(mockOnDeleteTask).toHaveBeenCalledWith(1);
  });

  it('cancels delete confirmation when No is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdateTask={mockOnUpdateTask}
        onDeleteTask={mockOnDeleteTask}
        onToggleTask={mockOnToggleTask}
      />
    );

    // Click delete button to show confirmation
    fireEvent.click(screen.getByText('🗑️'));

    // Click No to cancel
    fireEvent.click(screen.getByText('No'));

    expect(screen.queryByText('Yes')).not.toBeInTheDocument();
    expect(screen.queryByText('No')).not.toBeInTheDocument();
  });
});