# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo.config import cfg

from st2common import transport
from st2common.models.db.action import (runnertype_access, action_access, actionexec_access)
from st2common.models.db.action import actionexecstate_access
from st2common.persistence.base import (Access, ContentPackResourceMixin)


class RunnerType(Access):
    impl = runnertype_access

    @classmethod
    def _get_impl(cls):
        return cls.impl

    @classmethod
    def _get_by_object(cls, object):
        # For RunnerType name is unique.
        name = getattr(object, 'name', '')
        return cls.get_by_name(name)


class Action(Access, ContentPackResourceMixin):
    impl = action_access

    @classmethod
    def _get_impl(cls):
        return cls.impl


class ActionExecution(Access):
    impl = actionexec_access
    publisher = None

    @classmethod
    def _get_impl(cls):
        return cls.impl

    @classmethod
    def _get_publisher(cls):
        if not cls.publisher:
            cls.publisher = transport.actionexecution.ActionExecutionPublisher(
                cfg.CONF.messaging.url)
        return cls.publisher


class ActionExecutionState(Access):
    impl = actionexecstate_access
    publisher = None

    @classmethod
    def _get_impl(cls):
        return cls.impl

    @classmethod
    def _get_publisher(cls):
        if not cls.publisher:
            cls.publisher = transport.actionexecutionstate.ActionExecutionStatePublisher(
                cfg.CONF.messaging.url)
        return cls.publisher
