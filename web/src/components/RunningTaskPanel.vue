<template>
  <div>
    <div class="card">
      <div v-if="runningTask === undefined" class="card-body">
        <div class="d-flex bd-highlight">
          <h5 class="card-title">No running tasks</h5>
        </div>
      </div>
      <div v-if="runningTask !== undefined" class="card-body">
        <div class="d-flex bd-highlight">
          <h5 class="card-title">Currently Running: {{runningTask['task_desc']}}</h5>
          <span class="ml-auto"><i class="fa fa-cog fa-lg "></i></span>
        </div>
        <task-detail-info-handler :task="runningTask"></task-detail-info-handler>

      </div>
    </div>
  </div>
</template>

<script>
import TaskDetailInfoHandler from "./base/TaskDetailInfoHandler.vue";
export default {
  name: "RunningTaskPanel",
  props:["runningTask"],
  data:function (){
    return{
    }
  },
  components: {TaskDetailInfoHandler}
}
</script>

<style scoped>
.card-title{
  margin-bottom: 0;
}
.start-time{
  color: #999;
}
</style>