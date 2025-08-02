<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="d-flex bd-highlight">
          <h5 class="card-title">Waiting</h5>
        </div>
      </div>
      <TaskList v-bind:task-list="waitingTaskList" v-bind:no-data-label="'No waiting tasks'"></TaskList>
    </div>
  </div>
</template>

<script>
import TaskList from "./TaskList.vue"
export default {
  name: "WaitingTaskList",
  props:["waitingTaskList"],
  components: {TaskList},
  data:function (){
    return{
    }
  }
}
</script>

<style scoped>
  .card-body{
    border-bottom: 1px solid rgba(0,0,0,.125);
  }

</style>