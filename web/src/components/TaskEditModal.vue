<template>
  <div id="create-task-list-modal" class="modal fade" data-backdrop="static" data-keyboard="false">
    <div  class="modal-dialog modal-dialog-centered modal-xl">
      <div
        class="modal-content"
        :class="{ 'dimmed': showAoharuConfigModal || showSupportCardSelectModal }"
      >
        <h5 class="modal-header">
          Create New Task
        </h5>
        <div class="modal-body">
          <form>
            <div class="form-group">
              <label for="selectTaskType">⭐ Task Selection</label>
              <select v-model="selectedUmamusumeTaskType" class="form-control" id="selectTaskType">
                <option v-for="task in umamusumeTaskTypeList" :value="task">{{task.name}}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="selectExecuteMode">⭐ Execution Mode</label>
              <select v-model="selectedExecuteMode" class="form-control" id="selectExecuteMode">
                <option value=1>One-time</option>
              </select>
            </div>
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <label for="selectScenario">⭐ Scenario Selection</label>
                  <select v-model="selectedScenario" class="form-control" id="selectScenario">
                    <option :value="1">URA</option>
                    <option :value="2">Aoharu Cup</option>
                  </select>
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="selectUmamusume">Uma Musume Selection</label>
                  <select disabled class="form-control" id="selectUmamusume">
                    <option value=1>Use Last Selection</option>
                  </select>
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="selectAutoRecoverTP">Auto-recover when TP is low (Carrots only)</label>
                  <select v-model="recoverTP" class="form-control" id="selectAutoRecoverTP">
                    <option :value=true>Yes</option>
                    <option :value=false>No</option>
                  </select>
                </div>
              </div>
            </div>
            <!-- URA额外配置 -->
            <div class="row" v-if="selectedScenario === 1">
              <div class="col-4">
                <div class="form-group">
                  <span class="btn auto-btn ura-btn-bg" style="width: 100%; background-color:#6c757d;" v-on:click="openUraConfigModal">URA Configuration</span>
                </div>
              </div>
            </div>
            <!-- 青春杯额外配置 -->
            <div class="row" v-if="selectedScenario === 2">
              <div class="col-4">
                <div class="form-group">
                  <span class="btn auto-btn aoharu-btn-bg" style="width: 100%; background-color:#6c757d;" v-on:click="openAoharuConfigModal">Aoharu Cup Configuration</span>
                </div>
              </div>
            </div>
            <!-- 限时模块: 富士奇石的表演秀模式 -->
            <!-- <div class="row">
              <div class="col-3">
                <div class="form-group">
                  <label>⏰ 富士奇石的表演秀模式</label>
                  <select v-model="fujikisekiShowMode" class="form-control">
                    <option :value=true>是</option>
                    <option :value=false>否</option>
                  </select>
                </div>
              </div>
              <div class="col-2">
                <div class="form-group">
                  <label :style="{ color: fujikisekiShowMode ? '' : 'lightgrey' }">选择难度</label>
                  <select v-model="fujikisekiShowDifficulty" class="form-control" :disabled="!fujikisekiShowMode">
                    <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                  </select>
                </div>
              </div>
            </div> -->
            <div class="row">
              <div class="col-8">
                <div class="form-group">
                  <label for="race-select">⭐ Use Preset</label>
                    <div class="form-inline">
                      <select v-model="presetsUse" style="text-overflow: ellipsis;width: 40em;"  class="form-control" id="use_presets">
                        <option v-for="set in cultivatePresets" :value="set">{{set.name}}</option>
                      </select>
                      <span class="btn auto-btn ml-2" v-on:click="applyPresetRace">Apply</span>
                    </div>
                </div>
              </div>
              <div class="col-4">
                <div class="form-group">
                  <label for="presetNameEditInput">Save as Preset</label>
                  <div class="form-inline">
                    <input v-model="presetNameEdit" type="text" class="form-control" id="presetNameEditInput" placeholder="Preset Name">
                    <span class="btn auto-btn ml-2" v-on:click="addPresets">Save</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="row">
              <div class="col-5">
                <div class="form-group">
                  <label>⭐ Friend Support Card Selection</label>
                  <div style="display: flex; align-items: center;">
                    <input
                      type="text"
                      class="form-control"
                      :value="renderSupportCardText(selectedSupportCard)"
                      readonly
                      id="selectedSupportCard"
                    >
                    <span class="btn auto-btn ml-2" style="white-space:nowrap;" v-on:click="openSupportCardSelectModal">Change</span>
                  </div>
                </div>
              </div>
              <div class="col-2">
                <div class="form-group">
                  <label for="selectSupportCardLevel">Support Card Level (≥)</label>
                  <input v-model="supportCardLevel" type="number" class="form-control" id="selectSupportCardLevel" placeholder="">
                </div>
              </div>
              <div class="col-3">
                <div class="form-group">
                  <label for="inputClockUseLimit">Clock Usage Limit</label>
                  <input v-model="clockUseLimit" type="number" class="form-control" id="inputClockUseLimit" placeholder="">
                </div>
              </div>
            </div>
            <div class="form-group">
              <div>⭐ Target Attributes (If unsure about specific values, manually train once and input the final stats)</div>
            </div>
            <div class="row">
              <div class="col">
                <div class="form-group">
                    <label for="speed-value-input">Speed</label>
                    <input type="number" v-model="expectSpeedValue" class="form-control" id="speed-value-input">
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="stamina-value-input">Stamina</label>
                  <input type="number" v-model="expectStaminaValue" class="form-control" id="stamina-value-input">
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="power-value-input">Power</label>
                  <input type="number" v-model="expectPowerValue" class="form-control" id="power-value-input">
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="will-value-input">Guts</label>
                  <input type="number" v-model="expectWillValue" class="form-control" id="will-value-input">
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="intelligence-value-input">Wisdom</label>
                  <input type="number" v-model="expectIntelligenceValue" class="form-control" id="intelligence-value-input">
                </div>
              </div>
            </div>
            <div>
              <div class="form-group">
              <span v-if="!showAdvanceOption" class="btn auto-btn" style="width: 100%; background-color:#6c757d;" v-on:click="switchAdvanceOption">Show Advanced Options</span>
              <span v-if="showAdvanceOption" class="btn auto-btn" style="width: 100%; background-color:#6c757d;" v-on:click="switchAdvanceOption">Hide Advanced Options</span>
              </div>
            </div>
            <div v-if ="showAdvanceOption">
              <div class="form-group">
                <div>⭐ Extra Weight</div>
              </div>
              <p>Adjusts AI training preferences without affecting final target attributes. Generally used to prioritize certain training types. Weight range [-1.0 ~ 1.0], 0 means no extra weight applied.</p>
              <p>❗ Setting weight to -1 will skip that training</p>
              <p>❗ Within the same year, all weights cannot be -1</p>
              <p>When support cards or breeding stallion are weak, recommend increasing one attribute weight while decreasing others by the same amount</p>
              <div style="margin-bottom: 10px;">Year 1</div>
              <div class="row">
                <div v-for="v,i in extraWeight1" class="col">
                  <div class="form-group">
                    <input type="number"
                           v-model="extraWeight1[i]"
                           class="form-control"
                           @input="onExtraWeightInput(extraWeight1, i)"
                           id="speed-value-input">
                  </div>
                </div>
              </div>
              <div style="margin-bottom: 10px;">Year 2</div>
              <div class="row">
                <div v-for="v,i in extraWeight2" class="col">
                  <div class="form-group">
                    <input type="number"
                           v-model="extraWeight2[i]"
                           class="form-control"
                           @input="onExtraWeightInput(extraWeight2, i)"
                           id="speed-value-input">
                  </div>
                </div>
              </div>
              <div style="margin-bottom: 10px;">Year 3</div>
              <div class="row">
                <div v-for="v,i in extraWeight3" class="col">
                  <div class="form-group">
                    <input type="number"
                           v-model="extraWeight3[i]"
                           class="form-control"
                           @input="onExtraWeightInput(extraWeight3, i)"
                           id="speed-value-input">
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <div>⭐ Racing Style Selection</div>
            </div>
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <label for="selectTactic1">Year 1</label>
                  <select v-model="selectedRaceTactic1" class="form-control" id="selectTactic1">
                    <option :value=1>Stalker</option>
                    <option :value=2>Midfield</option>
                    <option :value=3>Front-runner</option>
                    <option :value=4>Pacesetter</option>
                  </select>
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="selectTactic2">Year 2</label>
                  <select v-model="selectedRaceTactic2" class="form-control" id="selectTactic2">
                    <option :value=1>Stalker</option>
                    <option :value=2>Midfield</option>
                    <option :value=3>Front-runner</option>
                    <option :value=4>Pacesetter</option>
                  </select>
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="selectTactic3">Year 3</label>
                  <select v-model="selectedRaceTactic3" class="form-control" id="selectTactic3">
                    <option :value=1>Stalker</option>
                    <option :value=2>Midfield</option>
                    <option :value=3>Front-runner</option>
                    <option :value=4>Pacesetter</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col">
                  <div class="form-group">
                    <label for="race-select">⭐ Additional Race Schedule</label>
                    <textarea type="text" disabled v-model="extraRace" class="form-control" id="race-select"></textarea>
                  </div>
                </div>
              </div>
              <div class="form-group">
              <span v-if="!showRaceList" class="btn auto-btn" style="width: 100%; background-color:#6c757d;" v-on:click="switchRaceList">Show Race Options</span>
              <span v-if="showRaceList" class="btn auto-btn" style="width: 100%; background-color:#6c757d;" v-on:click="switchRaceList">Hide Race Options</span>
              </div>
              <div class="row" v-if="showRaceList"> 
                <div class="col">
                  <div>Year 1</div>
                  <br/>
                  <div class="form-check">
                    <div v-for="race in umamusumeRaceList_1">
                      <input class="form-check-input position-static" v-model="extraRace" type="checkbox" :id="race.id" :value="race.id"><label :for="race.id" v-if="race.type==='GI'||race.type==='GII'&&!this.hideG2||race.type==='GIII'&&!this.hideG3">
                        <span v-if="race.type === 'GIII'">&nbsp;<span style="background-color: #58C471;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GII'">&nbsp;<span style="background-color: #F75A86;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GI'">&nbsp;<span style="background-color: #3485E3;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>{{race.date}} {{race.name}}</label>
                    </div>
                  </div>
                </div>
                <div class="col">
                  <div>Year 2</div>
                  <br/>
                  <div class="form-check">
                    <div v-for="race in umamusumeRaceList_2">
                      <input class="form-check-input position-static" v-model="extraRace" type="checkbox" :id="race.id" :value="race.id"><label :for="race.id" v-if="race.type==='GI'||race.type==='GII'&&!this.hideG2||race.type==='GIII'&&!this.hideG3">
                        <span v-if="race.type === 'GIII'">&nbsp;<span style="background-color: #58C471;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GII'">&nbsp;<span style="background-color: #F75A86;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GI'">&nbsp;<span style="background-color: #3485E3;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>{{race.date}} {{race.name}}</label>
                    </div>
                  </div>
                </div>
                <div class="col">
                  <div>Year 3</div>
                  <br/>
                  <div class="form-check">
                    <div v-for="race in umamusumeRaceList_3">
                      <input class="form-check-input position-static" v-model="extraRace" type="checkbox" :id="race.id" :value="race.id"><label :for="race.id" v-if="race.type==='GI'||race.type==='GII'&&!this.hideG2||race.type==='GIII'&&!this.hideG3">
                        <span v-if="race.type === 'GIII'">&nbsp;<span style="background-color: #58C471;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GII'">&nbsp;<span style="background-color: #F75A86;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>
                        <span v-if="race.type === 'GI'">&nbsp;<span style="background-color: #3485E3;" class="badge badge-pill badge-secondary">{{race.type}}</span>&nbsp;</span>{{race.date}} {{race.name}}</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-group mb-0">
              <div class="row">
                <div class="col">
                  <div class="form-group">
                    <label for="skill-learn">⭐ Skill Learning</label>
                  </div>
                </div>
              </div>
            </div>
            <div v-for="(item,index) in skillLearnPriorityList" :key="item.priority">
              <div class="form-group row">
                <label class="col-sm-3" for="'skill-learn-' + item.id">❗ Learning Priority {{ item.priority+1 }}</label>
                <div class="col-sm-6">
                  <textarea type="text"  v-model="item.skills" class="form-control" id="skill-learn-priority" placeholder="Corner Acceleration ◯, Slipstream, Hydrate, Speed Star, ... (use commas)"></textarea>
                </div>
                <div class="col-sm-3">
                  <span class="red-button auto-btn ml-2" v-on:click="deleteBox(item,index)">Delete Current Priority</span>
                </div>
              </div>
            </div>
            <span class="btn auto-btn ml-2" v-on:click="addBox(item)">Add Priority</span>
            <div class="form-group mb-0">
              <div class="row">
                <div class="col">
                  <div class="form-group">
                    <br>
                    <label for="skill-learn-default">✅ (All other unlisted skills fall under this priority)</label>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group mb-0">
              <div class="row">
                <div class="col">
                  <div class="form-group">
                    <label for="skill-learn-blacklist">⛔ Blacklist (Never learn these skills under any circumstances)</label>
                    <textarea type="text"  v-model="skillLearnBlacklist" class="form-control" id="skill-learn-blacklist" placeholder="Inner Post Proficiency ◯, Outer Post Proficiency ◯, Wet Conditions ◯, ... (skills to avoid)"></textarea>
                  </div>
                </div>
              </div>
            </div>
            

            <div class="form-group">
              <div class="row">
                <div class="col-3">
                  <div class="form-group">
                    <label for="learnSkillOnlyUserProvidedSelector">Only learn skills listed above during training</label>
                    <select v-model="learnSkillOnlyUserProvided" class="form-control" id="learnSkillOnlyUserProvidedSelector">
                      <option :value=true>Yes</option>
                      <option :value=false>No</option>
                    </select>
                  </div>
                </div>
                <div class="col-3">
                  <div class="form-group">
                    <label for="learnSkillBeforeRaceSelector">Learn skills before races</label>
                    <select disabled v-model="learnSkillBeforeRace" class="form-control" id="learnSkillBeforeRace">
                      <option :value=true>Yes</option>
                      <option :value=false>No</option>
                    </select>
                  </div>
                </div>
                <div class="col-3">
                  <div class="form-group">
                    <label for="inputSkillLearnThresholdLimit">Learn skills when skill points exceed this value</label>
                    <input v-model="learnSkillThreshold" type="number" class="form-control" id="inputSkillLearnThresholdLimit" placeholder="">
                  </div>
                </div>
              </div>
            </div>
          </form>
          <!-- <div class="part">
            <br>
                            <h6>Scheduled Settings</h6>
            <hr />
            <div class="row">
              <label for="cronInput" class="col-2 col-form-label">Cron Expression</label>
              <div class="col-10">
                <input v-model="cron"  class="form-control" id="cronInput">
              </div>
            </div>
          </div> -->
        </div>
        <div class="modal-footer">
          <span class="btn cancel-btn" v-on:click="cancelTask">Cancel</span>
          <span class="btn auto-btn" v-on:click="addTask">Confirm</span>
        </div>
      </div>
              <!-- Aoharu Cup Configuration Modal -->
      <AoharuConfigModal
        v-model:show="showAoharuConfigModal"
        :preliminaryRoundSelections="preliminaryRoundSelections"
        :aoharuTeamNameSelection="aoharuTeamNameSelection"
        @confirm="handleAoharuConfigConfirm"
      ></AoharuConfigModal>
      <!-- URA Configuration Modal -->
      <UraConfigModal
        v-model:show="showUraConfigModal"
        :skillEventWeight="skillEventWeight"
        :resetSkillEventWeightList="resetSkillEventWeightList"
        @confirm="handleUraConfigConfirm"
      ></UraConfigModal>
      <!-- Support Card Selection Modal -->
      <SupportCardSelectModal
        v-model:show="showSupportCardSelectModal"
        @cancel="closeSupportCardSelectModal"
        @confirm="handleSupportCardConfirm"
      ></SupportCardSelectModal>
      <!-- 遮罩层，支持两种弹窗 -->
      <div v-if="showAoharuConfigModal || showSupportCardSelectModal || showUraConfigModal" class="modal-backdrop-overlay" @click.stop></div>
      <!-- 通知 -->
      <div class="position-fixed" style="z-index: 5; right: 40%; width: 300px;">
        <div id="liveToast" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="2000">
          <div class="toast-body">
            ✔ Preset saved successfully
          </div>
        </div>
      </div>
      <!-- 权重警告通知 -->
      <div class="position-fixed" style="z-index: 5; right: 40%; width: 300px;">
        <div id="weightWarningToast" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="2000">
          <div class="toast-body" style="color: #856404;">
            ⚠️ <b>All weights in the same year cannot be -1</b>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SkillIcon from './SkillIcon.vue';
import AoharuConfigModal from './AoharuConfigModal.vue';
import UraConfigModal from './UraConfigModal.vue';
import SupportCardSelectModal from './SupportCardSelectModal.vue';

export default {
  name: "TaskEditModal",
  components: {
    SkillIcon,
    AoharuConfigModal,
    UraConfigModal,
    SupportCardSelectModal
  },
  data:function () {
    return{
      showAdvanceOption:false,
      showRaceList:false,
      dataReady:false,
      hideG2: false,
      hideG3: false,
      fujikisekiShowMode: false,
      fujikisekiShowDifficulty: 1,
      levelDataList:[],
      umamusumeTaskTypeList:[
        {
          id: 1,
          name: "Training",
        }
      ],
      umamusumeList:[
        {id:1, name:'特别周'},
        {id:2, name:'无声铃鹿'},
        {id:3, name:'东海帝王'},
        {id:4, name:'丸善斯基'},
        {id:5, name:'小栗帽'},
        {id:6, name:'大树快车'},
        {id:7, name:'目白麦昆'},
        {id:8, name:'好歌剧'},
        {id:9, name:'鲁道夫象征'},
        {id:10, name:'米浴'},
        {id:11, name:'黄金船'},
        {id:12, name:'伏特加'},
        {id:13, name:'大和赤骥'},
        {id:14, name:'草上飞'},
        {id:15, name:'神鹰'},
        {id:16, name:'气槽'},
        {id:17, name:'重炮'},
        {id:18, name:'超级小海湾'},
        {id:19, name:'目白赖恩'},
        {id:20, name:'爱丽速子'},
        {id:21, name:'胜利奖券'},
        {id:22, name:'樱花进王'},
        {id:23, name:'春乌拉拉'},
        {id:24, name:'待兼福来'},
        {id:25, name:'优秀素质'},
        {id:26, name:'帝王光环'},
      ],
              umamusumeRaceList_1:[
         {id:2004, name:'Hakodate Junior Stakes',date: 'Junior Year Late Jul', type: 'GIII'},
         {id:2009, name:'Niigata Junior Stakes',date: 'Junior Year Late Aug', type: 'GIII'},
         {id:2011, name:'Kokura Junior Stakes',date: 'Junior Year Early Sep', type: 'GIII'},
         {id:2013, name:'Sapporo Junior Stakes',date: 'Junior Year Early Sep', type: 'GIII'},
         {id:2022, name:'Saudi Arabia Royal Cup',date: 'Junior Year Early Oct', type: 'GIII'},
         {id:2024, name:'Artemis Stakes',date: 'Junior Year Late Oct', type: 'GIII'},
         {id:2028, name:'Daily Hai Junior Stakes',date: 'Junior Year Early Nov', type: 'GII'},
         {id:2032, name:'Keio Hai Junior Stakes',date: 'Junior Year Early Nov', type: 'GII'},
         {id:2029, name:'Fantasy Stakes',date: 'Junior Year Early Nov', type: 'GIII'},
         {id:2045, name:'Tokyo Sports Hai Junior Stakes',date: 'Junior Year Late Nov', type: 'GIII'},
         {id:2041, name:'Kyoto Junior Stakes',date: 'Junior Year Late Nov', type: 'GIII'},
         {id:2048, name:'Hanshin Juvenile Fillies', date: 'Junior Year Early Dec', type: 'GI'},
         {id:2046, name:'Asahi Hai Futurity Stakes', date: 'Junior Year Early Dec', type: 'GI'},
         {id:2052, name:'Hopeful Stakes', date: 'Junior Year Late Dec', type: 'GI'},
        ],
      umamusumeRaceList_2:[
         {id:2058, name:'Fairy Stakes',date: 'Classic Year Early Jan', type: 'GIII'},
         {id:2060, name:'Keisei Hai',date: 'Classic Year Early Jan', type: 'GIII'},
         {id:2062, name:'Shinzan Kinen',date: 'Classic Year Early Jan', type: 'GIII'},
         {id:2066, name:'Kisaragi Sho',date: 'Classic Year Early Feb', type: 'GIII'},
         {id:2067, name:'Kyodo News Hai',date: 'Classic Year Early Feb', type: 'GIII'},
         {id:2068, name:'Queen Cup',date: 'Classic Year Early Feb', type: 'GIII'},
         {id:2073, name:'Fillies\' Revue',date: 'Classic Year Early Mar', type: 'GII'},
         {id:2075, name:'Tulip Sho',date: 'Classic Year Early Mar', type: 'GII'},
         {id:2076, name:'Yayoi Sho',date: 'Classic Year Early Mar', type: 'GII'},
         {id:2078, name:'Flower Cup',date: 'Classic Year Late Mar', type: 'GIII'},
         {id:2079, name:'Spring Stakes',date: 'Classic Year Late Mar', type: 'GII'},
         {id:2077, name:'Falcon Stakes',date: 'Classic Year Late Mar', type: 'GIII'},
         {id:2081, name:'Mainichi Hai',date: 'Classic Year Late Mar', type: 'GIII'},
         {id:2085, name:'Oka Sho',date: 'Classic Year Early Apr', type: 'GI'},
         {id:2086, name:'Satsuki Sho',date: 'Classic Year Early Apr', type: 'GI'},
         {id:2084, name:'New Zealand Trophy',date: 'Classic Year Early Apr', type: 'GII'},
         {id:2082, name:'Arlington Cup',date: 'Classic Year Early Apr', type: 'GIII'},
         {id:2089, name:'Flora Stakes',date: 'Classic Year Late Apr', type: 'GII'},
         {id:2088, name:'Aoba Sho',date: 'Classic Year Late Apr', type: 'GII'},
         {id:2094, name:'NHK Mile Cup',date: 'Classic Year Early May', type: 'GI'},
         {id:2093, name:'Kyoto Shimbun Hai',date: 'Classic Year Early May', type: 'GII'},
         {id:2099, name:'Japanese Oaks',date: 'Classic Year Late May', type: 'GI'},
         {id:2101, name:'Tokyo Yushun (Japanese Derby)',date: 'Classic Year Late May', type: 'GI'},
         {id:2097, name:'Aoi Stakes',date: 'Classic Year Late May', type: 'GIII'},
         {id:2107, name:'Yasuda Kinen',date: 'Classic Year Early Jun', type: 'GI'},
         {id:2104, name:'Naruo Kinen',date: 'Classic Year Early Jun', type: 'GIII'},
         {id:2103, name:'Mermaid Stakes',date: 'Classic Year Early Jun', type: 'GIII'},
         {id:2102, name:'Epsom Cup',date: 'Classic Year Early Jun', type: 'GIII'},
         {id:2109, name:'Hakodate Sprint Stakes',date: 'Classic Year Late Jun', type: 'GIII'},
         {id:2114, name:'Unicorn Stakes',date: 'Classic Year Late Jun', type: 'GIII'},
         {id:2113, name:'Takarazuka Kinen',date: 'Classic Year Late Jun', type: 'GI'},
         {id:2116, name:'CBC Sho',date: 'Classic Year Early Jul', type: 'GIII'},
         {id:2117, name:'Hakodate Kinen',date: 'Classic Year Early Jul', type: 'GIII'},
         {id:2118, name:'Japan Dirt Derby',date: 'Classic Year Early Jul', type: 'GI'},
         {id:2121, name:'Procyon Stakes',date: 'Classic Year Early Jul', type: 'GIII'},
         {id:2122, name:'Radio Nikkei Sho',date: 'Classic Year Early Jul', type: 'GIII'},
         {id:2123, name:'Tanabata Sho',date: 'Classic Year Early Jul', type: 'GIII'},
         {id:2125, name:'Chukyo Kinen',date: 'Classic Year Late Jul', type: 'GIII'},
         {id:2127, name:'Ibis Summer Dash',date: 'Classic Year Late Jul', type: 'GIII'},
         {id:2128, name:'Queen Stakes',date: 'Classic Year Late Jul', type: 'GIII'},
         {id:2130, name:'Elm Stakes',date: 'Classic Year Early Aug', type: 'GIII'},
         {id:2132, name:'Kokura Kinen',date: 'Classic Year Early Aug', type: 'GIII'},
         {id:2135, name:'Sekiya Kinen',date: 'Classic Year Early Aug', type: 'GIII'},
         {id:2142, name:'Sapporo Kinen',date: 'Classic Year Late Aug', type: 'GII'},
         {id:2138, name:'Keeneland Cup',date: 'Classic Year Late Aug', type: 'GIII'},
         {id:2139, name:'Kitakyushu Kinen',date: 'Classic Year Late Aug', type: 'GIII'},
         {id:2144, name:'Centaur Stakes',date: 'Classic Year Early Sep', type: 'GII'},
         {id:2150, name:'Rose Stakes',date: 'Classic Year Early Sep', type: 'GII'},
         {id:2147, name:'Niigata Kinen',date: 'Classic Year Early Sep', type: 'GIII'},
         {id:2146, name:'Keisei Hai Autumn Handicap',date: 'Classic Year Early Sep', type: 'GIII'},
         {id:2151, name:'Shion Stakes',date: 'Classic Year Early Sep', type: 'GIII'},
         {id:2153, name:'All Comers',date: 'Classic Year Late Sep', type: 'GII'},
         {id:2154, name:'Kobe Shimbun Hai',date: 'Classic Year Late Sep', type: 'GII'},
         {id:2157, name:'Sirius Stakes',date: 'Classic Year Late Sep', type: 'GIII'},
         {id:2163, name:'Mainichi Okan',date: 'Classic Year Early Oct', type: 'GII'},
         {id:2164, name:'Kyoto Daishoten',date: 'Classic Year Early Oct', type: 'GII'},
         {id:2168, name:'Swan Stakes',date: 'Classic Year Late Oct', type: 'GII'},
         {id:2169, name:'Fuji Stakes',date: 'Classic Year Late Oct', type: 'GII'},
         {id:2172, name:'Tenno Sho (Autumn)',date: 'Classic Year Late Oct', type: 'GI'},
         {id:2173, name:'Shuka Sho',date: 'Classic Year Late Oct', type: 'GI'},
         {id:2174, name:'Kikuka Sho',date: 'Classic Year Late Oct', type: 'GI'},
         {id:2176, name:'Argentina Kyowa Hai',date: 'Classic Year Early Nov', type: 'GII'},
         {id:2181, name:'Elizabeth Queen Cup',date: 'Classic Year Early Nov', type: 'GI'},
         {id:2182, name:'Japan Breeders\' Cup Classic',date: 'Classic Year Early Nov', type: 'GI'},
         {id:2183, name:'Japan Breeders\' Cup Sprint',date: 'Classic Year Early Nov', type: 'GI'},
         {id:2184, name:'Japan Breeders\' Cup Filly & Mare Turf',date: 'Classic Year Early Nov', type: 'GI'},
         {id:2185, name:'Keihan Hai',date: 'Classic Year Late Nov', type: 'GIII'},
         {id:2188, name:'Mile Championship',date: 'Classic Year Late Nov', type: 'GI'},
         {id:2189, name:'Japan Cup',date: 'Classic Year Late Nov', type: 'GI'},
         {id:2191, name:'Stayers Stakes',date: 'Classic Year Early Dec', type: 'GII'},
         {id:2194, name:'Capella Stakes',date: 'Classic Year Early Dec', type: 'GIII'},
         {id:2195, name:'Turquoise Stakes',date: 'Classic Year Early Dec', type: 'GIII'},
         {id:2196, name:'Champions Cup',date: 'Classic Year Early Dec', type: 'GI'},
         {id:2197, name:'Hanshin Cup',date: 'Classic Year Late Dec', type: 'GII'},
         {id:2201, name:'Nakayama Daishoten',date: 'Classic Year Late Dec', type: 'GI'},
         {id:2203, name:'Tokyo Daishoten',date: 'Classic Year Late Dec', type: 'GI'},
      ],
      umamusumeRaceList_3:[
         {id:2213, name:'Kyoto Kimpai',date: 'Senior Year Early Jan', type: 'GIII'},
         {id:2215, name:'Nakayama Kimpai',date: 'Senior Year Early Jan', type: 'GIII'},
         {id:2210, name:'Aichi Hai',date: 'Senior Year Early Jan', type: 'GIII'},
         {id:2217, name:'Nikkei Shinshun Hai',date: 'Senior Year Early Jan', type: 'GII'},
         {id:2225, name:'Tokai Stakes',date: 'Senior Year Late Jan', type: 'GII'},
         {id:2220, name:'American JCC',date: 'Senior Year Late Jan', type: 'GII'},
         {id:2223, name:'Silk Road Stakes',date: 'Senior Year Late Jan', type: 'GIII'},
         {id:2221, name:'Negishi Stakes',date: 'Senior Year Late Jan', type: 'GIII'},
         {id:2227, name:'Kyoto Kinen',date: 'Senior Year Early Feb', type: 'GII'},
         {id:2229, name:'Tokyo Shimbun Hai',date: 'Senior Year Early Feb', type: 'GIII'},
         {id:2238, name:'Nakayama Kinen',date: 'Senior Year Late Feb', type: 'GII'},
         {id:2237, name:'Kyoto Umamusume Stakes',date: 'Senior Year Late Feb', type: 'GIII'},
         {id:2231, name:'Diamond Stakes',date: 'Senior Year Late Feb', type: 'GIII'},
         {id:2235, name:'Kokura Daishoten',date: 'Senior Year Late Feb', type: 'GIII'},
         {id:2234, name:'Hankyu Hai',date: 'Senior Year Late Feb', type: 'GIII'},
         {id:2233, name:'February Stakes',date: 'Senior Year Late Feb', type: 'GI'},
         {id:2240, name:'Kinko Sho',date: 'Senior Year Early Mar', type: 'GII'},
         {id:2244, name:'Ocean Stakes',date: 'Senior Year Early Mar', type: 'GIII'},
         {id:2242, name:'Nakayama Umamusume Stakes',date: 'Senior Year Early Mar', type: 'GIII'},
         {id:2248, name:'Hanshin Daishoten',date: 'Senior Year Late Mar', type: 'GII'},
         {id:2250, name:'Nikkei Sho',date: 'Senior Year Late Mar', type: 'GII'},
         {id:2249, name:'March Stakes',date: 'Senior Year Late Mar', type: 'GIII'},
         {id:2253, name:'Takamatsunomiya Kinen',date: 'Senior Year Late Mar', type: 'GI'},
         {id:2251, name:'Osaka Hai',date: 'Senior Year Late Mar', type: 'GI'},
         {id:2258, name:'Hanshin Umamusume Stakes',date: 'Senior Year Early Apr', type: 'GII'},
         {id:2260, name:'Lord Derby Challenge Trophy',date: 'Senior Year Early Apr', type: 'GIII'},
         {id:2254, name:'Antares Stakes',date: 'Senior Year Early Apr', type: 'GIII'},
         {id:2263, name:'Milers Cup',date: 'Senior Year Late Apr', type: 'GII'},
         {id:2262, name:'Fukushima Umamusume Stakes',date: 'Senior Year Late Apr', type: 'GIII'},
         {id:2265, name:'Tenno Sho (Spring)',date: 'Senior Year Late Apr', type: 'GI'},
         {id:2268, name:'Keio Hai Spring Cup',date: 'Senior Year Early May', type: 'GII'},
         {id:2272, name:'Niigata Daishoten',date: 'Senior Year Early May', type: 'GIII'},
         {id:2275, name:'Victoria Mile',date: 'Senior Year Early May', type: 'GI'},
         {id:2281, name:'Meguro Kinen',date: 'Senior Year Late May', type: 'GII'},
         {id:2277, name:'Heian Stakes',date: 'Senior Year Late May', type: 'GIII'},
         {id:2283, name:'Mermaid Stakes',date: 'Senior Year Early Jun', type: 'GIII'},
         {id:2287, name:'Yasuda Kinen',date: 'Senior Year Early Jun', type: 'GI'},
         {id:2284, name:'Naruo Kinen',date: 'Senior Year Early Jun', type: 'GIII'},
         {id:2282, name:'Epsom Cup',date: 'Senior Year Early Jun', type: 'GIII'},
         {id:2293, name:'Takarazuka Kinen',date: 'Senior Year Late Jun', type: 'GI'},
         {id:2289, name:'Hakodate Sprint Stakes',date: 'Senior Year Late Jun', type: 'GIII'},
         {id:2294, name:'Teio Sho',date: 'Senior Year Late Jun', type: 'GI'},
         {id:2296, name:'CBC Sho',date: 'Senior Year Early Jul', type: 'GIII'},
         {id:2300, name:'Procyon Stakes',date: 'Senior Year Early Jul', type: 'GIII'},
         {id:2301, name:'Tanabata Sho',date: 'Senior Year Early Jul', type: 'GIII'},
         {id:2297, name:'Hakodate Kinen',date: 'Senior Year Early Jul', type: 'GIII'},
         {id:2303, name:'Chukyo Kinen',date: 'Senior Year Late Jul', type: 'GIII'},
         {id:2305, name:'Ibis Summer Dash',date: 'Senior Year Late Jul', type: 'GIII'},
         {id:2306, name:'Queen Stakes',date: 'Senior Year Late Jul', type: 'GIII'},
         {id:2308, name:'Elm Stakes',date: 'Senior Year Early Aug', type: 'GIII'},
         {id:2315, name:'Sapporo Kinen',date: 'Senior Year Late Aug', type: 'GII'},
         {id:2317, name:'Keeneland Cup',date: 'Senior Year Late Aug', type: 'GIII'},
         {id:2318, name:'Kitakyushu Kinen',date: 'Senior Year Late Aug', type: 'GIII'},
         {id:2321, name:'Centaur Stakes',date: 'Senior Year Early Sep', type: 'GII'},
         {id:2324, name:'Niigata Kinen',date: 'Senior Year Early Sep', type: 'GIII'},
         {id:2323, name:'Keisei Hai Autumn Handicap',date: 'Senior Year Early Sep', type: 'GIII'},
         {id:2330, name:'All Comers',date: 'Senior Year Late Sep', type: 'GII'},
         {id:2331, name:'Kobe Shimbun Hai',date: 'Senior Year Late Sep', type: 'GII'},
         {id:2334, name:'Sirius Stakes',date: 'Senior Year Late Sep', type: 'GIII'},
         {id:2340, name:'Mainichi Okan',date: 'Senior Year Early Oct', type: 'GII'},
         {id:2341, name:'Kyoto Daishoten',date: 'Senior Year Early Oct', type: 'GII'},
         {id:2345, name:'Swan Stakes',date: 'Senior Year Late Oct', type: 'GII'},
         {id:2346, name:'Fuji Stakes',date: 'Senior Year Late Oct', type: 'GII'},
         {id:2349, name:'Tenno Sho (Autumn)',date: 'Senior Year Late Oct', type: 'GI'},
         {id:2353, name:'Argentina Kyowa Hai',date: 'Senior Year Early Nov', type: 'GII'},
         {id:2358, name:'Elizabeth Queen Cup',date: 'Senior Year Early Nov', type: 'GI'},
         {id:2359, name:'Japan Breeders\' Cup Classic',date: 'Senior Year Early Nov', type: 'GI'},
         {id:2360, name:'Japan Breeders\' Cup Sprint',date: 'Senior Year Early Nov', type: 'GI'},
         {id:2361, name:'Japan Breeders\' Cup Filly & Mare Turf',date: 'Senior Year Early Nov', type: 'GI'},
         {id:2362, name:'Keihan Hai',date: 'Senior Year Late Nov', type: 'GIII'},
         {id:2365, name:'Mile Championship',date: 'Senior Year Late Nov', type: 'GI'},
         {id:2366, name:'Japan Cup',date: 'Senior Year Late Nov', type: 'GI'},
         {id:2368, name:'Stayers Stakes',date: 'Senior Year Early Dec', type: 'GII'},
         {id:2371, name:'Capella Stakes',date: 'Senior Year Early Dec', type: 'GIII'},
         {id:2372, name:'Turquoise Stakes',date: 'Senior Year Early Dec', type: 'GIII'},
         {id:2373, name:'Champions Cup',date: 'Senior Year Early Dec', type: 'GI'},
         {id:2374, name:'Hanshin Cup',date: 'Senior Year Late Dec', type: 'GII'},
         {id:2378, name:'Nakayama Daishoten',date: 'Senior Year Late Dec', type: 'GI'},
         {id:2380, name:'Tokyo Daishoten',date: 'Senior Year Late Dec', type: 'GI'}],
      cultivatePresets:[],
      cultivateDefaultPresets:[
      {
          name: "默认",
          race_list: [],
          skill: "",
          skill_priority_list:[],
          expect_attribute:[800, 800, 800, 400, 400],
          follow_support_card: {id:10001, name:'在耀眼景色的前方', desc:'无声铃鹿'},
          follow_support_card_level: 50,
          clock_use_limit: 99,
          learn_skill_threshold: 9999,
          race_tactic_1: 4,
          race_tactic_2: 4,
          race_tactic_3: 4,

        },
        {
          name: "小栗帽基础育成赛程",
          race_list: [1701, 2303, 2401, 5208, 5407, 5904],
          skill: "",
          skill_priority_list:[],
          expect_attribute:[800, 650, 800, 300, 400],
          follow_support_card: {id:20004, name:'一颗安心糖', desc:'超级溪流'},
          follow_support_card_level: 50,
          clock_use_limit: 99,
          learn_skill_threshold: 9999,
          race_tactic_1: 4,
          race_tactic_2: 4,
          race_tactic_3: 4,
        },
        {
          name: "大和赤骥基础育成赛程",
          race_list: [1701, 2303],
          skill: "",
          skill_priority_list:[],
          expect_attribute:[800, 600, 600, 300, 400],
          follow_support_card: {id:20004, name:'一颗安心糖', desc:'超级溪流'},
          follow_support_card_level: 50,
          clock_use_limit: 99,
          learn_skill_threshold: 9999,
          race_tactic_1: 4,
          race_tactic_2: 4,
          race_tactic_3: 4,
        },
        {
          name: "目白麦昆基础育成赛程",
          race_list: [2203, 2401],
          skill: "",
          skill_priority_list:[],
          expect_attribute:[700, 700, 600, 350, 400],
          follow_support_card: {id:20004, name:'一颗安心糖', desc:'超级溪流'},
          follow_support_card_level: 50,
          clock_use_limit: 99,
          learn_skill_threshold: 9999,
          race_tactic_1: 4,
          race_tactic_2: 4,
          race_tactic_3: 4,
        },
        {
          name:"历战小栗帽35战60w粉丝(需求觉醒3,借满破小海湾,种马速耐,支援卡带赛后加成高的)",
          race_list:[1601,1701,1902,2103,2302,2401,2701,2905,3103,3303,3404,3601,4102,4203,4408,4506,4607,4804,4902,5208,5407,5601,5709,5904,6006,6602,6701,6807,7007,7111,7204],
          skill:"大胃王",
          skill_priority_list:[],
          expect_attribute:[700,500,700,350,350],
          follow_support_card: {id:20004, name:'一颗安心糖', desc:'超级溪流'},
          follow_support_card_level:50,
          clock_use_limit:2,
          learn_skill_threshold:450,
          race_tactic_1:4,
          race_tactic_2:3,
          race_tactic_3:3
        }
      ],
      expectSpeedValue : 650,
      expectStaminaValue : 600,
      expectPowerValue: 650,
      expectWillValue: 300,
      expectIntelligenceValue:300,

      supportCardLevel: 50,
      
      presetsUse: {
          name: "默认",
          race_list: [],
          skill: "",
          skill_priority_list:[],
          skill_blacklist: "",
          expect_attribute:[650, 800, 650, 400, 400],
          follow_support_card: {id:10001, name:'在耀眼景色的前方', desc:'无声铃鹿'},
          follow_support_card_level: 50,
          clock_use_limit: 99,
          learn_skill_threshold: 9999,
          race_tactic_1: 4,
          race_tactic_2: 4,
          race_tactic_3: 4,
          extraWeight:[],
        },
      // ===  已选择  ===
      selectedExecuteMode: 1,
      expectTimes: 0,
      cron: "* * * * *",
      
      selectedScenario: 1,
      selectedUmamusumeTaskType: undefined,
      selectedSupportCard: undefined,
      extraRace: [],
      skillLearnPriorityList:[
					{
						priority:0,
						skills:""
					}
				],
      skillPriorityNum:1,
      skillLearnBlacklist:"",
      learnSkillOnlyUserProvided: false,
      learnSkillBeforeRace: false,
      selectedRaceTactic1: 4,
      selectedRaceTactic2: 4,
      selectedRaceTactic3: 4,
      clockUseLimit: 99,
      learnSkillThreshold: 9999,
      recoverTP: false,
      presetNameEdit: "",
      successToast: undefined,
      extraWeight1: [0, 0, 0, 0, 0],
      extraWeight2: [0, 0, 0, 0, 0],
      extraWeight3: [0, 0, 0, 0, 0],

      // URA配置
      skillEventWeight: [0, 0, 0],
      resetSkillEventWeightList: '',

      // 青春杯配置
      preliminaryRoundSelections: [2, 1, 1, 1],
      aoharuTeamNameSelection: 4,
      showAoharuConfigModal: false,
      showUraConfigModal: false,
      showSupportCardSelectModal: false,      
    }
  },
  mounted() {
    this.initSelect()
    this.getPresets()
    this.successToast = $('#liveToast').toast({})
  },
  methods:{
    deleteBox(item,index){
        if(this.skillLearnPriorityList.length<=1){
          return false
        }
        this.skillLearnPriorityList.splice(index,1)
        this.skillPriorityNum--
        for(let i = index; i < this.skillPriorityNum; i++)
        {
          this.skillLearnPriorityList[i].priority--
        }
      },
    addBox(item){
        if(this.skillLearnPriorityList.length>=5)
        {
          return false
        }
        this.skillLearnPriorityList.push(
          {
            priority:this.skillPriorityNum++,
            skills:''
          }
        )
    },
    initSelect: function (){
      this.selectedSupportCard = {id:10001, name:'在耀眼景色的前方', desc:'无声铃鹿'}
      this.selectedUmamusumeTaskType = this.umamusumeTaskTypeList[0]
    },
    switchRaceList: function(){
      this.showRaceList = !this.showRaceList
    },
    switchAdvanceOption: function(){
      this.showAdvanceOption = !this.showAdvanceOption
    },
    openUraConfigModal: function(){
      this.showUraConfigModal = true;
    },
    closeUraConfigModal: function(){
      this.showUraConfigModal = false;
    },
    openAoharuConfigModal: function(){
      this.showAoharuConfigModal = true;
    },
    closeAoharuConfigModal: function(){
      this.showAoharuConfigModal = false;
    },
    handleUraConfigConfirm: function(data) {
      this.skillEventWeight = [...data.skillEventWeight];
      this.resetSkillEventWeightList = data.resetSkillEventWeightList;
      this.showUraConfigModal = false;
    },
    handleAoharuConfigConfirm: function(data) {
      this.preliminaryRoundSelections = [...data.preliminaryRoundSelections];
      this.aoharuTeamNameSelection = data.aoharuTeamNameSelection;
      this.showAoharuConfigModal = false;
    },
    cancelTask: function(){
      $('#create-task-list-modal').modal('hide');
    },
    addTask: function (){
      var learn_skill_list = []
      for (let i = 0; i < this.skillPriorityNum; i++)
      {
        if(String(this.skillLearnPriorityList[i].skills) != "")
        {
          learn_skill_list.push(String(this.skillLearnPriorityList[i].skills).split(",").map(item => item.trim()))
        }
      }
      console.log(learn_skill_list)
      var learn_skill_blacklist = this.skillLearnBlacklist ? this.skillLearnBlacklist.split(",").map(item => item.trim()) : []
      var ura_reset_skill_event_weight_list = this.resetSkillEventWeightList ? this.resetSkillEventWeightList.split(",").map(item => item.trim()) : []
      let payload = {
        app_name: "umamusume",
        task_execute_mode: this.selectedExecuteMode,
        task_type: this.selectedUmamusumeTaskType.id,
        task_desc: this.selectedUmamusumeTaskType.name,
        attachment_data: {
          "scenario": this.selectedScenario,
          "expect_attribute": [this.expectSpeedValue, this.expectStaminaValue, this.expectPowerValue, this.expectWillValue, this.expectIntelligenceValue],
          "follow_support_card_name": this.selectedSupportCard.name,
          "follow_support_card_level": this.supportCardLevel,
          "extra_race_list": this.extraRace,
          "learn_skill_list": learn_skill_list,
          "learn_skill_blacklist": learn_skill_blacklist,
          "tactic_list": [this.selectedRaceTactic1, this.selectedRaceTactic2, this.selectedRaceTactic3],
          "clock_use_limit": this.clockUseLimit,
          "learn_skill_threshold": this.learnSkillThreshold,
          "allow_recover_tp": this.recoverTP,
          "learn_skill_only_user_provided": this.learnSkillOnlyUserProvided,
          "extra_weight": [this.extraWeight1, this.extraWeight2, this.extraWeight3],
          // 限时: 富士奇石的表演秀
          "fujikiseki_show_mode": this.fujikisekiShowMode,
          "fujikiseki_show_difficulty": this.fujikisekiShowDifficulty,
          // URA配置
          "ura_config": this.selectedScenario === 1 ? {
            "skillEventWeight": [...this.skillEventWeight],
            "resetSkillEventWeightList": ura_reset_skill_event_weight_list
          } : null,
          // 青春杯配置
          "aoharu_config": this.selectedScenario === 2 ? {
            "preliminaryRoundSelections": [...this.preliminaryRoundSelections],
            "aoharuTeamNameSelection": this.aoharuTeamNameSelection
          } : null
        },
        cron_job_info:{},
      }
      if(this.selectedExecuteMode === 2){
        payload.cron_job_info = {
          cron: this.cron
        }
      }
      console.log(JSON.stringify(payload))
      this.axios.post("/task", JSON.stringify(payload)).then(
          ()=>{
            $('#create-task-list-modal').modal('hide');
          }
      )
    },
    applyPresetRace: function(){
      this.selectedScenario = this.presetsUse.scenario || 1
      this.extraRace = this.presetsUse.race_list
      this.expectSpeedValue = this.presetsUse.expect_attribute[0]
      this.expectStaminaValue = this.presetsUse.expect_attribute[1]
      this.expectPowerValue = this.presetsUse.expect_attribute[2]
      this.expectWillValue = this.presetsUse.expect_attribute[3]
      this.expectIntelligenceValue = this.presetsUse.expect_attribute[4]
      this.selectedSupportCard = this.presetsUse.follow_support_card,
      this.supportCardLevel = this.presetsUse.follow_support_card_level,
      this.clockUseLimit = this.presetsUse.clock_use_limit,
      this.learnSkillThreshold = this.presetsUse.learn_skill_threshold,
      this.selectedRaceTactic1 = this.presetsUse.race_tactic_1,
      this.selectedRaceTactic2 = this.presetsUse.race_tactic_2,
      this.selectedRaceTactic3 = this.presetsUse.race_tactic_3,
      this.skillLearnBlacklist = this.presetsUse.skill_blacklist

      if ('extraWeight' in this.presetsUse && this.presetsUse.extraWeight != [])
      {
        this.extraWeight1 =  this.presetsUse.extraWeight[0].map(v => Math.max(-1, Math.min(1, v)));
        this.extraWeight2 =  this.presetsUse.extraWeight[1].map(v => Math.max(-1, Math.min(1, v)));
        this.extraWeight3 =  this.presetsUse.extraWeight[2].map(v => Math.max(-1, Math.min(1, v)));
      }
      else
      {
        this.extraWeight1 = [0,0,0,0,0]
        this.extraWeight2 = [0,0,0,0,0]
        this.extraWeight3 = [0,0,0,0,0]
      }
      if ('skill' in this.presetsUse && this.presetsUse.skill != "")
      {
        this.skillLearnPriorityList[0].skills = this.presetsUse.skill
        while(this.skillPriorityNum > 1)
        {
          this.deleteBox(0,this.skillPriorityNum-1)
        }
      }
      else
      {
        for (let i = 0; i < this.presetsUse.skill_priority_list.length; i++)
        {
          if (i >= this.skillPriorityNum)
          {
            this.addBox()
          }
          this.skillLearnPriorityList[i].skills = this.presetsUse.skill_priority_list[i]
        }
        while(this.presetsUse.skill_priority_list.length != 0 &&
              this.skillPriorityNum > this.presetsUse.skill_priority_list.length)
        {
          this.deleteBox(0,this.skillPriorityNum-1)
        }
      }
      
      // 读取青春杯配置（如果存在）
      if ('ura_config' in this.presetsUse) {
        this.skillEventWeight = [...this.presetsUse.ura_config.skillEventWeight];
        this.resetSkillEventWeightList = this.presetsUse.ura_config.resetSkillEventWeightList;
      } else {
        this.skillEventWeight = [0, 0, 0];
        this.resetSkillEventWeightList = '';
      }
      if ('auharuhai_config' in this.presetsUse) {
        this.preliminaryRoundSelections = [...this.presetsUse.auharuhai_config.preliminaryRoundSelections];
        this.aoharuTeamNameSelection = this.presetsUse.auharuhai_config.aoharuTeamNameSelection;
      } else {
        this.preliminaryRoundSelections = [2, 1, 1, 1];
        this.aoharuTeamNameSelection = 4;
      }
      
    },
    getPresets: function(){
      this.axios.post("/umamusume/get-presets", "").then(
          res=>{
          let tmplist = []
          tmplist = tmplist.concat(this.cultivateDefaultPresets)
          tmplist = tmplist.concat(res.data)
          this.cultivatePresets = tmplist
        }
      )
    },
    addPresets: function(){
      let preset = {
        name: this.presetNameEdit,
        scenario: this.selectedScenario,
        race_list: this.extraRace,
        skill_priority_list: [],
        skill_blacklist: this.skillLearnBlacklist,
        expect_attribute:[this.expectSpeedValue, this.expectStaminaValue, this.expectPowerValue, this.expectWillValue, this.expectIntelligenceValue],
        follow_support_card: this.selectedSupportCard,
        follow_support_card_level: this.supportCardLevel,
        clock_use_limit: this.clockUseLimit,
        learn_skill_threshold: this.learnSkillThreshold,
        race_tactic_1: this.selectedRaceTactic1,
        race_tactic_2: this.selectedRaceTactic2,
        race_tactic_3: this.selectedRaceTactic3,
        extraWeight: [
          this.extraWeight1.map(v => Math.max(-1, Math.min(1, v))),
          this.extraWeight2.map(v => Math.max(-1, Math.min(1, v))),
          this.extraWeight3.map(v => Math.max(-1, Math.min(1, v)))
        ]
      }
      // 仅当剧本对应时, 添加URA或青春杯配置
      if (this.selectedScenario === 1) {
        preset.ura_config = {
          skillEventWeight: [...this.skillEventWeight],
          resetSkillEventWeightList: this.resetSkillEventWeightList
        };
      } else if (this.selectedScenario === 2) {
        preset.auharuhai_config = {
          preliminaryRoundSelections: [...this.preliminaryRoundSelections],
          aoharuTeamNameSelection: this.aoharuTeamNameSelection
        };
      }
      for(let i = 0; i < this.skillPriorityNum; i++)
      {
        if(this.skillLearnPriorityList[i].skills != "")
        {
          preset.skill_priority_list.push([this.skillLearnPriorityList[i].skills])
        }
      }
      let payload = {
        "preset": JSON.stringify(preset)
      }
      console.log(JSON.stringify(payload))
      this.axios.post("/umamusume/add-presets", JSON.stringify(payload)).then(
        ()=>{
          this.successToast.toast('show')
          this.getPresets()
        } 
      )
    },
    onExtraWeightInput(arr, idx) {
      // 限制输入范围 [-1, 1]
      if (arr[idx] > 1) arr[idx] = 1;
      if (arr[idx] < -1) arr[idx] = -1;
      // 检查是否全为-1，若是则重置最后一个输入为0并弹出警告
      if (arr.filter(v => v === -1).length === arr.length) {
        arr[idx] = 0;
        // 显示警告通知
        this.showWeightWarning();
      }
    },
    showWeightWarning() {
      let warnToast = document.getElementById('weightWarningToast');
      if (warnToast) {
        warnToast.classList.remove('hide');
        warnToast.classList.add('show');
        setTimeout(() => {
          warnToast.classList.remove('show');
          warnToast.classList.add('hide');
        }, 2000);
      }
    },
    openSupportCardSelectModal: function() {
      this.showSupportCardSelectModal = true;
    },
    closeSupportCardSelectModal: function() {
      this.showSupportCardSelectModal = false;
    },
    handleSupportCardConfirm(card) {
      this.selectedSupportCard = card;
      this.showSupportCardSelectModal = false;
    },
    renderSupportCardText(card) {
      if (!card) return '';
      let type = '';
      if (card.id >= 10000 && card.id < 20000) type = '速';
      else if (card.id >= 20000 && card.id < 30000) type = '耐';
      else if (card.id >= 30000 && card.id < 40000) type = '力';
      else if (card.id >= 40000 && card.id < 50000) type = '根';
      else if (card.id >= 50000 && card.id < 60000) type = '智';
      if (type) {
        return `【${card.name}】${type}·${card.desc}`;
      } else {
        return `【${card.name}】${card.desc}`;
      }
    },
  },
  watch:{

  }
}
</script>

<style scoped>

.btn{
  padding: 0.4rem 0.8rem !important;
  font-size: 1rem !important;
}

.red-button {
  background-color: red !important;
  padding: 0.4rem 0.8rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
}

/* 取消按钮样式 */
.cancel-btn {
  background-color: #dc3545 !important; /* Bootstrap的danger红色 */
  color: white !important;
  padding: 0.4rem 0.8rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
  margin-right: 10px; /* 与确认按钮间距 */
  border: none;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #c82333 !important; /* 悬停时更深的红色 */
  color: white !important;
}

/* 确保modal body可以正确滚动 */
.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

/* 遮罩层样式 - 让TaskEditModal背景变暗并阻止交互 */
.modal-backdrop-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1055; /* 确保在TaskEditModal之上，但在AoharuConfigModal之下 */
  pointer-events: auto; /* 阻止与背景元素的交互 */
}

/* 只有青春杯配置弹窗时让TaskEditModal变暗 */
#create-task-list-modal.modal.show .modal-content {
  transition: opacity 0.3s ease;
}

#create-task-list-modal.modal.show .modal-content.dimmed {
  opacity: 0.6;
}

.aoharu-btn-bg {
  background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('../assets/img/scenario/aoharu_btn_bg.png') center center no-repeat;
  background-size: cover;
  background-position: center -50px;
  color: #ffffff !important;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  font-weight: 600;
  padding: 0.5rem 1rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
  width: 100%;
  min-height: 40px;
  display: inline-block;
  transition: all 0.3s ease;
}

.ura-btn-bg {
  background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('../assets/img/scenario/ura_btn_bg.png') center center no-repeat;
  background-size: cover;
  background-position: center -100px;
  color: #ffffff !important;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  font-weight: 600;
  padding: 0.5rem 1rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
  width: 100%;
  min-height: 40px;
  display: inline-block;
  transition: all 0.3s ease;
}
</style>