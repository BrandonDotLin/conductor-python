from __future__ import annotations
from typing import List
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.http.models.workflow_task import WorkflowTask


class DynamicForkTask(TaskInterface):
    _pre_fork_task: TaskInterface
    _join_task: JoinTask

    def __init__(self, task_ref_name: str, pre_fork_task: TaskInterface, join_task: JoinTask = None) -> DynamicForkTask:
        super().__init__(task_ref_name, TaskType.INLINE)
        self._pre_fork_task = pre_fork_task
        self._join_task = join_task

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.dynamic_fork_join_tasks_param = 'forkedTasks'
        workflow.dynamic_fork_tasks_input_param_name = 'forkedTasksInputs'
        workflow.input_parameters['forkedTasks'] = self._pre_fork_task.output_ref(
            'forkedTasks')
        workflow.input_parameters['forkedTasksInputs'] = self._pre_fork_task.output_ref(
            'forkedTasksInputs')
        tasks = [
            self._pre_fork_task.to_workflow_task(),
            workflow,
        ]
        if self._join_task != None:
            tasks.append(self._join_task.to_workflow_task())
        return tasks
