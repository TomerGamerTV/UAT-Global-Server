<template>
  <div>
    <div v-if="task.task_type === 1">
      <div>
        <span>Scenario: {{ scenarioName }}</span>
      </div>
      <div>
        <span>Target Stats: {{task.detail?.expect_attribute}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UmamusumeTaskDetailInfo",
  props: ["task"],
  computed: {
    scenarioName() {
      if (this.task.detail?.scenario === 1) {
        return 'URA';
      } else if (this.task.detail?.scenario === 2) {
        return 'Aoharu Cup';
      }
      return 'Unknown Scenario';
    }
  }
}
</script>