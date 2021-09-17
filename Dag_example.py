
"""Example DAG demonstrating the usage of the BranchPythonOperator."""

import random

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.edgemodifier import Label

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='example_branch_operator',
    default_args=args,
    start_date=days_ago(2),
    schedule_interval="@daily",
    tags=['example', 'example2'],
) as dag:

    run_this_first = DummyOperator(
        task_id='run_this_first',
    )

    options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=lambda: random.choice(options),
    )
    run_this_first >> branching

    join = DummyOperator(
        task_id='join',
        trigger_rule='none_failed_or_skipped',
    )

    for option in options:
        t = DummyOperator(
            task_id=option,
        )

        dummy_follow = DummyOperator(
            task_id='follow_' + option,
        )

        # Label is optional here, but it can help identify more complex branches
        branching >> Label(option) >> t >> dummy_follow >> join
