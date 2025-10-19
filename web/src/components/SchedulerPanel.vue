<template>
  <div class="list-panel">
    <div class="mb-3">
      <auto-status-panel></auto-status-panel>
    </div>
    <div class="mb-3">
      <running-task-panel :running-task="runningTask"></running-task-panel>
    </div>
    <div class="mb-3">
      <waiting-task-list :waiting-task-list="waitingTaskList"></waiting-task-list>
    </div>
    <div class="mb-3">
      <history-task-list :history-task-list="historyTaskList"></history-task-list>
    </div>
    <div class="mb-3">
      <div class="card image-card">
        <div class="card-body">
          <div class="image-layer" :style="{ '--image-url': `url(${imageBg})` }"></div>
        </div>
      </div>
    </div>
    <div>
      <task-edit-modal></task-edit-modal>
    </div>
  </div>
</template>

<script>
import RunningTaskPanel from "@/components/RunningTaskPanel.vue";
import WaitingTaskList from "@/components/WaitingTaskList.vue";
import AutoStatusPanel from "@/components/AutoStatusPanel.vue";
import TaskEditModal from "@/components/TaskEditModal.vue";
import HistoryTaskList from "@/components/HistoryTaskList.vue";
import CronJobList from "@/components/CronJobList.vue";
import imageBgUrl from "../../assets/cunny.png";
export default {
  name: "SchedulerPanel",
  components: { CronJobList, HistoryTaskList, TaskEditModal, WaitingTaskList, AutoStatusPanel, RunningTaskPanel },
  props: ["runningTask", "waitingTaskList", "historyTaskList", "cronJobList"],
  data(){ return { imageBg: imageBgUrl } }
}
</script>

<style scoped>
.list-panel{display:flex;flex-direction:column;height:100%}
.list-panel .card{margin-bottom:0}
.image-card{flex:1 1 auto;display:flex}
.image-card .card-body{height:392px;min-height:392px;flex:0 0 auto;border-radius:12px;overflow:hidden}
.image-card .image-layer{width:100%;height:100%;min-height:100%;background:transparent var(--image-url) center/contain no-repeat !important}
.list-panel> .mb-3:last-child{margin-bottom:0}
.list-title{font-weight:700}
.list-empty{color:var(--muted)}
</style>