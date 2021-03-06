# Copyright 2018 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from airflow.models import DAG
from airflow.operators import DrydockDeployNodesOperator
from airflow.operators import DrydockPrepareNodesOperator
from airflow.operators import DrydockPrepareSiteOperator
from airflow.operators import DrydockVerifySiteOperator

from config_path import config_path


def deploy_site_drydock(parent_dag_name, child_dag_name, args):
    '''
    DryDock Subdag
    '''
    dag = DAG(
        '{}.{}'.format(parent_dag_name, child_dag_name),
        default_args=args)

    drydock_verify_site = DrydockVerifySiteOperator(
        task_id='verify_site',
        shipyard_conf=config_path,
        main_dag_name=parent_dag_name,
        sub_dag_name=child_dag_name,
        dag=dag)

    drydock_prepare_site = DrydockPrepareSiteOperator(
        task_id='prepare_site',
        shipyard_conf=config_path,
        main_dag_name=parent_dag_name,
        sub_dag_name=child_dag_name,
        dag=dag)

    drydock_prepare_nodes = DrydockPrepareNodesOperator(
        task_id='prepare_nodes',
        shipyard_conf=config_path,
        main_dag_name=parent_dag_name,
        sub_dag_name=child_dag_name,
        dag=dag)

    drydock_deploy_nodes = DrydockDeployNodesOperator(
        task_id='deploy_nodes',
        shipyard_conf=config_path,
        main_dag_name=parent_dag_name,
        sub_dag_name=child_dag_name,
        dag=dag)

    # Define dependencies
    drydock_prepare_site.set_upstream(drydock_verify_site)
    drydock_prepare_nodes.set_upstream(drydock_prepare_site)
    drydock_deploy_nodes.set_upstream(drydock_prepare_nodes)

    return dag
