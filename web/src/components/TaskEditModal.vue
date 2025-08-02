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
              <div v-if="showRaceList">
                <!-- Race Filter Controls -->
                <div class="row mb-3">
                  <div class="col-md-4">
                    <label>🔍 Search Races:</label>
                    <input type="text" v-model="raceSearch" class="form-control" placeholder="Search by race name...">
                  </div>
                  <div class="col-md-4">
                    <label>👤 Character Filter:</label>
                    <select v-model="selectedCharacter" class="form-control" @change="onCharacterChange">
                      <option value="">All Characters</option>
                      <option v-for="character in characterList" :key="character.name" :value="character.name">{{character.name}}</option>
                    </select>
                  </div>
                  <div class="col-md-4">
                    <label>🏁 Quick Selection:</label>
                    <div class="btn-group" role="group">
                      <button type="button" class="btn btn-sm btn-outline-success" @click="selectAllGI">Select All GI</button>
                      <button type="button" class="btn btn-sm btn-outline-success" @click="selectAllGII">Select All GII</button>
                      <button type="button" class="btn btn-sm btn-outline-success" @click="selectAllGIII">Select All GIII</button>
                      <button type="button" class="btn btn-sm btn-outline-warning" @click="clearAllRaces">Clear All</button>
                    </div>
                  </div>
                </div>
                
                <!-- Filter Buttons -->
                <div class="row mb-3">
                  <div class="col-md-3">
                    <label>🏆 Grade:</label>
                    <div class="btn-group btn-group-sm d-flex" role="group">
                      <button type="button" class="btn" :class="{'btn-primary': showGI, 'btn-outline-primary': !showGI}" @click="showGI = !showGI">
                        <span style="background-color: #3485E3; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">GI</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-primary': showGII, 'btn-outline-primary': !showGII}" @click="showGII = !showGII">
                        <span style="background-color: #F75A86; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">GII</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-primary': showGIII, 'btn-outline-primary': !showGIII}" @click="showGIII = !showGIII">
                        <span style="background-color: #58C471; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">GIII</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-primary': showOP, 'btn-outline-primary': !showOP}" @click="showOP = !showOP">
                        <span style="background-color: #FFA500; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">OP</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-primary': showPREOP, 'btn-outline-primary': !showPREOP}" @click="showPREOP = !showPREOP">
                        <span style="background-color: #9370DB; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">PRE-OP</span>
                      </button>
                  </div>
                </div>
                  <div class="col-md-3">
                    <label>🌱 Terrain:</label>
                    <div class="btn-group btn-group-sm d-flex" role="group">
                      <button type="button" class="btn" :class="{'btn-success': showTurf, 'btn-outline-success': !showTurf}" @click="showTurf = !showTurf">
                        <span style="background-color: #28a745; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Turf</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-warning': showDirt, 'btn-outline-warning': !showDirt}" @click="showDirt = !showDirt">
                        <span style="background-color: #ffc107; color: black; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Dirt</span>
                      </button>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label>📏 Distance:</label>
                    <div class="btn-group btn-group-sm d-flex" role="group">
                      <button type="button" class="btn" :class="{'btn-info': showSprint, 'btn-outline-info': !showSprint}" @click="showSprint = !showSprint">
                        <span style="background-color: #17a2b8; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Sprint</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-info': showMile, 'btn-outline-info': !showMile}" @click="showMile = !showMile">
                        <span style="background-color: #17a2b8; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Mile</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-info': showMedium, 'btn-outline-info': !showMedium}" @click="showMedium = !showMedium">
                        <span style="background-color: #17a2b8; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Medium</span>
                      </button>
                      <button type="button" class="btn" :class="{'btn-info': showLong, 'btn-outline-info': !showLong}" @click="showLong = !showLong">
                        <span style="background-color: #17a2b8; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px;">Long</span>
                      </button>
                    </div>
                  </div>
                </div>
                
                

                <!-- Race Lists -->
                <div class="row"> 
                  <div class="col-md-4">
                    <div class="card">
                      <div class="card-header">
                        <h6 class="mb-0">Year 1 (Junior Year)</h6>
                      </div>
                                              <div class="card-body" style="max-height: 400px; overflow-y: auto;">
                          <div class="race-grid">
                            <div v-for="race in filteredRaces_1" :key="race.id" 
                                 class="race-toggle" 
                                 :class="{ 'selected': extraRace.includes(race.id) }"
                                 @click="toggleRace(race.id)">
                              <div class="race-content">
                                <div class="race-name">{{race.name}}</div>
                                <div class="race-badges">
                                  <span v-if="race.type === 'G3'" class="badge badge-pill" style="background-color: #58C471;">{{race.type}}</span>
                                  <span v-if="race.type === 'G2'" class="badge badge-pill" style="background-color: #F75A86;">{{race.type}}</span>
                                  <span v-if="race.type === 'G1'" class="badge badge-pill" style="background-color: #3485E3;">{{race.type}}</span>
                                  <span v-if="race.type === 'OP'" class="badge badge-pill" style="background-color: #FFA500;">{{race.type}}</span>
                                  <span v-if="race.type === 'PRE-OP'" class="badge badge-pill" style="background-color: #9370DB;">{{race.type}}</span>
                                  <span v-if="race.terrain === 'Turf'" class="badge badge-pill" style="background-color: #28a745; color: white;">{{race.terrain}}</span>
                                  <span v-if="race.terrain === 'Dirt'" class="badge badge-pill" style="background-color: #ffc107; color: black;">{{race.terrain}}</span>
                                  <span v-if="race.distance === 'Sprint'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Mile'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Medium'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Long'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                </div>
                                <div class="race-details">{{race.date}} • {{race.venue}}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="card">
                      <div class="card-header">
                        <h6 class="mb-0">Year 2 (Classic Year)</h6>
                      </div>
                                              <div class="card-body" style="max-height: 400px; overflow-y: auto;">
                          <div class="race-grid">
                            <div v-for="race in filteredRaces_2" :key="race.id" 
                                 class="race-toggle" 
                                 :class="{ 'selected': extraRace.includes(race.id) }"
                                 @click="toggleRace(race.id)">
                              <div class="race-content">
                                <div class="race-name">{{race.name}}</div>
                                <div class="race-badges">
                                  <span v-if="race.type === 'G3'" class="badge badge-pill" style="background-color: #58C471;">{{race.type}}</span>
                                  <span v-if="race.type === 'G2'" class="badge badge-pill" style="background-color: #F75A86;">{{race.type}}</span>
                                  <span v-if="race.type === 'G1'" class="badge badge-pill" style="background-color: #3485E3;">{{race.type}}</span>
                                  <span v-if="race.type === 'OP'" class="badge badge-pill" style="background-color: #FFA500;">{{race.type}}</span>
                                  <span v-if="race.type === 'PRE-OP'" class="badge badge-pill" style="background-color: #9370DB;">{{race.type}}</span>
                                  <span v-if="race.terrain === 'Turf'" class="badge badge-pill" style="background-color: #28a745; color: white;">{{race.terrain}}</span>
                                  <span v-if="race.terrain === 'Dirt'" class="badge badge-pill" style="background-color: #ffc107; color: black;">{{race.terrain}}</span>
                                  <span v-if="race.distance === 'Sprint'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Mile'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Medium'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Long'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                </div>
                                <div class="race-details">{{race.date}} • {{race.venue}}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="card">
                      <div class="card-header">
                        <h6 class="mb-0">Year 3 (Senior Year)</h6>
                      </div>
                                              <div class="card-body" style="max-height: 400px; overflow-y: auto;">
                          <div class="race-grid">
                            <div v-for="race in filteredRaces_3" :key="race.id" 
                                 class="race-toggle" 
                                 :class="{ 'selected': extraRace.includes(race.id) }"
                                 @click="toggleRace(race.id)">
                              <div class="race-content">
                                <div class="race-name">{{race.name}}</div>
                                <div class="race-badges">
                                  <span v-if="race.type === 'G3'" class="badge badge-pill" style="background-color: #58C471;">{{race.type}}</span>
                                  <span v-if="race.type === 'G2'" class="badge badge-pill" style="background-color: #F75A86;">{{race.type}}</span>
                                  <span v-if="race.type === 'G1'" class="badge badge-pill" style="background-color: #3485E3;">{{race.type}}</span>
                                  <span v-if="race.type === 'OP'" class="badge badge-pill" style="background-color: #FFA500;">{{race.type}}</span>
                                  <span v-if="race.type === 'PRE-OP'" class="badge badge-pill" style="background-color: #9370DB;">{{race.type}}</span>
                                  <span v-if="race.terrain === 'Turf'" class="badge badge-pill" style="background-color: #28a745; color: white;">{{race.terrain}}</span>
                                  <span v-if="race.terrain === 'Dirt'" class="badge badge-pill" style="background-color: #ffc107; color: black;">{{race.terrain}}</span>
                                  <span v-if="race.distance === 'Sprint'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Mile'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Medium'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                  <span v-if="race.distance === 'Long'" class="badge badge-pill" style="background-color: #17a2b8; color: white;">{{race.distance}}</span>
                                </div>
                                <div class="race-details">{{race.date}} • {{race.venue}}</div>
                              </div>
                            </div>
                          </div>
                        </div>
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
            
            <!-- Priority 0 Skills (Best) -->
            <div class="form-group">
              <label class="form-label">🏆 Priority 0 - SS Tier Skills (Best)</label>
              <div class="skill-grid">
                <div v-for="skill in skillPriority0" :key="skill" 
                     class="skill-toggle" 
                     :class="{ 'selected': selectedSkills.includes(skill) }"
                     @click="toggleSkill(skill)">
                  <div class="skill-content">
                    <div class="skill-name">{{skill}}</div>
                    <div class="skill-priority">SS Tier</div>
                </div>
                </div>
              </div>
            </div>

            <!-- Priority 1 Skills (Good) -->
                  <div class="form-group">
              <label class="form-label">🥇 Priority 1 - S/A Tier Skills (Good)</label>
              <div class="skill-grid">
                <div v-for="skill in skillPriority1" :key="skill" 
                     class="skill-toggle" 
                     :class="{ 'selected': selectedSkills.includes(skill) }"
                     @click="toggleSkill(skill)">
                  <div class="skill-content">
                    <div class="skill-name">{{skill}}</div>
                    <div class="skill-priority">S/A Tier</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Priority 2 Skills (Situational) -->
                  <div class="form-group">
              <label class="form-label">🥈 Priority 2 - B Tier Skills (Situational)</label>
              <div class="skill-grid">
                <div v-for="skill in skillPriority2" :key="skill" 
                     class="skill-toggle" 
                     :class="{ 'selected': selectedSkills.includes(skill) }"
                     @click="toggleSkill(skill)">
                  <div class="skill-content">
                    <div class="skill-name">{{skill}}</div>
                    <div class="skill-priority">B Tier</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Blacklist Section -->
            <div class="form-group">
              <label class="form-label">⛔ Blacklist (Never learn these skills)</label>
              <div class="skill-grid">
                <div v-for="skill in skillPriority2" :key="skill" 
                     class="skill-toggle blacklist-toggle" 
                     :class="{ 'selected': blacklistedSkills.includes(skill) }"
                     @click="toggleBlacklistSkill(skill)">
                  <div class="skill-content">
                    <div class="skill-name">{{skill}}</div>
                    <div class="skill-priority">Blacklisted</div>
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
      // Race filtering properties
      raceSearch: '',
      showGI: true,
      showGII: true,
      showGIII: true,
      showOP: true,
      showPREOP: true,
      showTurf: true,
      showDirt: true,
      showSprint: true,
      showMile: true,
      showMedium: true,
      showLong: true,
      // Character filter properties
      selectedCharacter: '',
      characterList: [],
      characterAptitudes: {},
      characterTrainingPeriods: {},
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
        {id:1, name:'Special Week'},
        {id:2, name:'Silence Suzuka'},
        {id:3, name:'Tokai Teio'},
        {id:4, name:'Maruzensky'},
        {id:5, name:'Oguri Cap'},
        {id:6, name:'Taiki Shuttle'},
        {id:7, name:'Mejiro Mcqueen'},
        {id:8, name:'TM Opera O'},
        {id:9, name:'Symboli Rudolf'},
        {id:10, name:'Rice Shower'},
        {id:11, name:'Gold Ship'},
        {id:12, name:'Vodka'},
        {id:13, name:'Daiwa Scarlet'},
        {id:14, name:'Glass Wonder'},
        {id:15, name:'El Condor Pasa'},
        {id:16, name:'Air Groove'},
        {id:17, name:'Mayano Top Gun'},
        {id:18, name:'Super Creek'},
        {id:19, name:'Mejiro Ryan'},
        {id:20, name:'Agnes Tachyon'},
        {id:21, name:'Winning Ticket'},
        {id:22, name:'Sakura Bakushin O'},
        {id:23, name:'Haru Urara'},
        {id:24, name:'Matikanefukukitaru'},
        {id:25, name:'Nice Nature'},
        {id:26, name:'King Halo'},
      ],
      // Character data from aptitude_output.csv and character_objective_ranges.csv
      characterList: [
        {name: 'Agnes Tachyon', terrain: 'Turf', distance: 'Medium'},
        {name: 'Air Groove', terrain: 'Turf', distance: 'Medium'},
        {name: 'Biwa Hayahide', terrain: 'Turf', distance: 'Medium'},
        {name: 'Curren Chan', terrain: 'Turf', distance: 'Sprint'},
        {name: 'Daiwa Scarlet', terrain: 'Turf', distance: 'Mile'},
        {name: 'El Condor Pasa', terrain: 'Turf', distance: 'Mile'},
        {name: 'Gold Ship', terrain: 'Turf', distance: 'Medium'},
        {name: 'Grass Wonder', terrain: 'Turf', distance: 'Mile'},
        {name: 'Haru Urara', terrain: 'Dirt', distance: 'Sprint'},
        {name: 'King Halo', terrain: 'Turf', distance: 'Sprint'},
        {name: 'Maruzensky', terrain: 'Turf', distance: 'Mile'},
        {name: 'Matikanefukukitaru', terrain: 'Turf', distance: 'Medium'},
        {name: 'Mayano Top Gun', terrain: 'Turf', distance: 'Medium'},
        {name: 'Mejiro McQueen', terrain: 'Turf', distance: 'Medium'},
        {name: 'Mejiro Ryan', terrain: 'Turf', distance: 'Medium'},
        {name: 'Mihono Bourbon', terrain: 'Turf', distance: 'Medium'},
        {name: 'Nice Nature', terrain: 'Turf', distance: 'Medium'},
        {name: 'Oguri Cap', terrain: 'Turf', distance: 'Mile'},
        {name: 'Rice Shower', terrain: 'Turf', distance: 'Medium'},
        {name: 'Sakura Bakushin O', terrain: 'Turf', distance: 'Sprint'},
        {name: 'Silence Suzuka', terrain: 'Turf', distance: 'Mile'},
        {name: 'Special Week', terrain: 'Turf', distance: 'Medium'},
        {name: 'Super Creek', terrain: 'Turf', distance: 'Medium'},
        {name: 'Symboli Rudolf', terrain: 'Turf', distance: 'Medium'},
        {name: 'Taiki Shuttle', terrain: 'Turf', distance: 'Sprint'},
        {name: 'TM Opera O', terrain: 'Turf', distance: 'Medium'},
        {name: 'Tokai Teio', terrain: 'Turf', distance: 'Medium'},
        {name: 'Vodka', terrain: 'Turf', distance: 'Mile'},
        {name: 'Winning Ticket', terrain: 'Turf', distance: 'Medium'}
      ],
      // Character training periods from character_objective_ranges.csv
      characterTrainingPeriods: {
        'Agnes Tachyon': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'King Halo': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Early Oct']
        },
        'Curren Chan': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep']
        },
        'Daiwa Scarlet': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'El Condor Pasa': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        },
        'Gold Ship': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Grass Wonder': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Haru Urara': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Early Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Maruzensky': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct']
        },
        'Matikanefukukitaru': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Mayano Top Gun': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Super Creek': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Air Groove': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct']
        },
        'Biwa Hayahide': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Symboli Rudolf': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        },
        'Taiki Shuttle': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov']
        },
        'TM Opera O': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        },
        'Tokai Teio': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        },
        'Vodka': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Late May', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct']
        },
        'Winning Ticket': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Mejiro McQueen': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct']
        },
        'Mejiro Ryan': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Mihono Bourbon': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        },
        'Nice Nature': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov']
        },
        'Oguri Cap': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Early Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Rice Shower': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Late Nov', 'Senior Year Early Dec']
        },
        'Sakura Bakushin O': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Early Feb', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov']
        },
        'Silence Suzuka': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Late Feb', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Late May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Early Oct', 'Classic Year Late Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Late Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep']
        },
        'Special Week': {
          'Junior Year': ['Junior Year Early Jul', 'Junior Year Late Jul', 'Junior Year Early Aug', 'Junior Year Late Aug', 'Junior Year Early Sep', 'Junior Year Late Sep', 'Junior Year Early Oct', 'Junior Year Late Oct', 'Junior Year Early Nov', 'Junior Year Late Nov', 'Junior Year Early Dec', 'Junior Year Late Dec'],
          'Classic Year': ['Classic Year Pre-Debut', 'Classic Year Early Jan', 'Classic Year Late Jan', 'Classic Year Late Feb', 'Classic Year Early Mar', 'Classic Year Late Mar', 'Classic Year Early Apr', 'Classic Year Late Apr', 'Classic Year Early May', 'Classic Year Early Jun', 'Classic Year Late Jun', 'Classic Year Early Jul', 'Classic Year Late Jul', 'Classic Year Early Aug', 'Classic Year Late Aug', 'Classic Year Early Sep', 'Classic Year Late Sep', 'Classic Year Early Oct', 'Classic Year Early Nov', 'Classic Year Late Nov', 'Classic Year Early Dec', 'Classic Year Late Dec'],
          'Senior Year': ['Senior Year Pre-Debut', 'Senior Year Early Jan', 'Senior Year Late Jan', 'Senior Year Early Feb', 'Senior Year Late Feb', 'Senior Year Early Mar', 'Senior Year Late Mar', 'Senior Year Early Apr', 'Senior Year Early May', 'Senior Year Late May', 'Senior Year Early Jun', 'Senior Year Late Jun', 'Senior Year Early Jul', 'Senior Year Late Jul', 'Senior Year Early Aug', 'Senior Year Late Aug', 'Senior Year Early Sep', 'Senior Year Late Sep', 'Senior Year Early Oct', 'Senior Year Late Oct', 'Senior Year Early Nov', 'Senior Year Early Dec']
        }
      },
              umamusumeRaceList_1:[
              {id:2003, name:'Chukyo Junior Stakes',date: 'Junior Year Late Jul', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Chukyo'},
              {id:2004, name:'Hakodate Junior Stakes',date: 'Junior Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Hakodate'},
              {id:2005, name:'Cosmos Sho',date: 'Junior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Sapporo'},
              {id:2006, name:'Dahlia Sho',date: 'Junior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
              {id:2007, name:'Phoenix Sho',date: 'Junior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kokura'},
              {id:2008, name:'Clover Sho',date: 'Junior Year Late Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Sapporo'},
              {id:2009, name:'Niigata Junior Stakes',date: 'Junior Year Late Aug', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
              {id:2010, name:'Aster Sho',date: 'Junior Year Early Sep', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
              {id:2011, name:'Kokura Junior Stakes',date: 'Junior Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kokura'},
              {id:2012, name:'Nojigiku Stakes',date: 'Junior Year Early Sep', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
              {id:2013, name:'Sapporo Junior Stakes',date: 'Junior Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Sapporo'},
              {id:2014, name:'Suzuran Sho',date: 'Junior Year Early Sep', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Sapporo'},
              {id:2015, name:'Canna Stakes',date: 'Junior Year Late Sep', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
              {id:2016, name:'Fuyo Stakes',date: 'Junior Year Late Sep', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
              {id:2017, name:'Kikyo Stakes',date: 'Junior Year Late Sep', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
              {id:2018, name:'Saffron Sho',date: 'Junior Year Late Sep', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
              {id:2019, name:'Momiji Stakes',date: 'Junior Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
              {id:2020, name:'Platanus Sho',date: 'Junior Year Early Oct', type: 'PRE-OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
              {id:2021, name:'Rindo Sho',date: 'Junior Year Early Oct', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
              {id:2022, name:'Saudi Arabia Royal Cup',date: 'Junior Year Early Oct', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2023, name:'Shigiku Sho',date: 'Junior Year Early Oct', type: 'PRE-OP', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
              {id:2024, name:'Artemis Stakes',date: 'Junior Year Late Oct', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2025, name:'Hagi Stakes',date: 'Junior Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
              {id:2026, name:'Ivy Stakes',date: 'Junior Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2027, name:'Nadeshiko Sho',date: 'Junior Year Late Oct', type: 'PRE-OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
              {id:2028, name:'Daily Hai Junior Stakes',date: 'Junior Year Early Nov', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
              {id:2029, name:'Fantasy Stakes',date: 'Junior Year Early Nov', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
              {id:2030, name:'Fukushima Junior Stakes',date: 'Junior Year Early Nov', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Fukushima'},
              {id:2031, name:'Hyakunichiso Tokubetsu',date: 'Junior Year Early Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
              {id:2032, name:'Keio Hai Junior Stakes',date: 'Junior Year Early Nov', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
              {id:2033, name:'Kigiku Sho',date: 'Junior Year Early Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
              {id:2034, name:'Kimmokusei Tokubetsu',date: 'Junior Year Early Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Fukushima'},
              {id:2035, name:'Oxalis Sho',date: 'Junior Year Early Nov', type: 'PRE-OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
              {id:2036, name:'Akamatsu Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2037, name:'Begonia Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2038, name:'Cattleya Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
              {id:2039, name:'Habotan Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
              {id:2040, name:'Koyamaki Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Chukyo'},
              {id:2041, name:'Kyoto Junior Stakes',date: 'Junior Year Late Nov', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
              {id:2042, name:'Mochinoki Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
              {id:2043, name:'Shiragiku Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
              {id:2044, name:'Shumeigiku Sho',date: 'Junior Year Late Nov', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
              {id:2045, name:'Tokyo Sports Hai Junior Stakes',date: 'Junior Year Late Nov', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
              {id:2046, name:'Asahi Hai Futurity Stakes',date: 'Junior Year Early Dec', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
              {id:2047, name:'Erica Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
              {id:2048, name:'Hanshin Juvenile Fillies',date: 'Junior Year Early Dec', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
              {id:2049, name:'Hiiragi Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
              {id:2050, name:'Kantsubaki Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Chukyo'},
              {id:2051, name:'Kuromatsu Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
              {id:2052, name:'Manryo Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
              {id:2053, name:'Sazanka Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
              {id:2054, name:'Tsuwabuki Sho',date: 'Junior Year Early Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Sprint', venue: 'Chukyo'},
              {id:2055, name:'Christmas Rose Stakes',date: 'Junior Year Late Dec', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
              {id:2056, name:'Hopeful Stakes',date: 'Junior Year Late Dec', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
              {id:2057, name:'Senryo Sho',date: 'Junior Year Late Dec', type: 'PRE-OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
        ],
      umamusumeRaceList_2:[
      {id:2058, name:'Fairy Stakes',date: 'Classic Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2059, name:'Junior Cup',date: 'Classic Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2060, name:'Keisei Hai',date: 'Classic Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2061, name:'Kobai Stakes',date: 'Classic Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2062, name:'Shinzan Kinen',date: 'Classic Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2063, name:'Crocus Stakes',date: 'Classic Year Late Jan', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2064, name:'Wakagoma Stakes',date: 'Classic Year Late Jan', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2065, name:'Elfin Stakes',date: 'Classic Year Early Feb', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2066, name:'Kisaragi Sho',date: 'Classic Year Early Feb', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2067, name:'Kyodo News Hai',date: 'Classic Year Early Feb', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2068, name:'Queen Cup',date: 'Classic Year Early Feb', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2069, name:'Hyacinth Stakes',date: 'Classic Year Late Feb', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2070, name:'Marguerite Stakes',date: 'Classic Year Late Feb', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2071, name:'Sumire Stakes',date: 'Classic Year Late Feb', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2072, name:'Anemone Stakes',date: 'Classic Year Early Mar', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2073, name:'Fillies/Revue',date: 'Classic Year Early Mar', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2074, name:'Shoryu Stakes',date: 'Classic Year Early Mar', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Chukyo'},
      {id:2075, name:'Tulip Sho',date: 'Classic Year Early Mar', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2076, name:'Yayoi Sho',date: 'Classic Year Early Mar', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2077, name:'Falcon Stakes',date: 'Classic Year Late Mar', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Chukyo'},
      {id:2078, name:'Flower Cup',date: 'Classic Year Late Mar', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2079, name:'Mainichi Hai',date: 'Classic Year Late Mar', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2080, name:'Spring Stakes',date: 'Classic Year Late Mar', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2081, name:'Wakaba Stakes',date: 'Classic Year Late Mar', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2082, name:'Arlington Cup',date: 'Classic Year Early Apr', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2083, name:'Fukuryu Stakes',date: 'Classic Year Early Apr', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2084, name:'New Zealand Trophy',date: 'Classic Year Early Apr', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2085, name:'Oka Sho',date: 'Classic Year Early Apr', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2086, name:'Satsuki Sho',date: 'Classic Year Early Apr', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2087, name:'Wasurenagusa Sho',date: 'Classic Year Early Apr', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2088, name:'Aoba Sho',date: 'Classic Year Late Apr', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2089, name:'Flora Stakes',date: 'Classic Year Late Apr', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2090, name:'Sweetpea Stakes',date: 'Classic Year Late Apr', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2091, name:'Tachibana Stakes',date: 'Classic Year Late Apr', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2092, name:'Tango Stakes',date: 'Classic Year Late Apr', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2093, name:'Kyoto Shimbun Hai',date: 'Classic Year Early May', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2094, name:'NHK Mile Cup',date: 'Classic Year Early May', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2095, name:'Principal Stakes',date: 'Classic Year Early May', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2096, name:'Seiryu Stakes',date: 'Classic Year Early May', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2097, name:'Aoi Stakes',date: 'Classic Year Late May', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2098, name:'Hosu Stakes',date: 'Classic Year Late May', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
      {id:2099, name:'Japanese Oaks',date: 'Classic Year Late May', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2100, name:'Shirayuri Stakes',date: 'Classic Year Late May', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2101, name:'Tokyo Yushun (Japanese Derby)',date: 'Classic Year Late May', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2102, name:'Epsom Cup',date: 'Classic Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2103, name:'Mermaid Stakes',date: 'Classic Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2104, name:'Naruo Kinen',date: 'Classic Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2105, name:'Sleipnir Stakes',date: 'Classic Year Early Jun', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Tokyo'},
      {id:2106, name:'Tempozan Stakes',date: 'Classic Year Early Jun', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2107, name:'Yasuda Kinen',date: 'Classic Year Early Jun', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2108, name:'Akhalteke Stakes',date: 'Classic Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2109, name:'Hakodate Sprint Stakes',date: 'Classic Year Late Jun', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Hakodate'},
      {id:2110, name:'Onuma Stakes',date: 'Classic Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hakodate'},
      {id:2111, name:'Paradise Stakes',date: 'Classic Year Late Jun', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2112, name:'Sannomiya Stakes',date: 'Classic Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hanshin'},
      {id:2113, name:'Takarazuka Kinen',date: 'Classic Year Late Jun', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2114, name:'Unicorn Stakes',date: 'Classic Year Late Jun', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2115, name:'Yonago Stakes',date: 'Classic Year Late Jun', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2116, name:'CBC Sho',date: 'Classic Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Chukyo'},
      {id:2117, name:'Hakodate Kinen',date: 'Classic Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hakodate'},
      {id:2118, name:'Japan Dirt Derby',date: 'Classic Year Early Jul', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
      {id:2119, name:'Marine Stakes',date: 'Classic Year Early Jul', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hakodate'},
      {id:2120, name:'Meitetsu Hai',date: 'Classic Year Early Jul', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Chukyo'},
      {id:2121, name:'Procyon Stakes',date: 'Classic Year Early Jul', type: 'G3', terrain: 'Dirt', distance: 'Sprint', venue: 'Chukyo'},
      {id:2122, name:'Radio Nikkei Sho',date: 'Classic Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Fukushima'},
      {id:2123, name:'Tanabata Sho',date: 'Classic Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Fukushima'},
      {id:2124, name:'Tomoe Sho',date: 'Classic Year Early Jul', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hakodate'},
      {id:2125, name:'Chukyo Kinen',date: 'Classic Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Chukyo'},
      {id:2126, name:'Fukushima TV Open',date: 'Classic Year Late Jul', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Fukushima'},
      {id:2127, name:'Ibis Summer Dash',date: 'Classic Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2128, name:'Queen Stakes',date: 'Classic Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Sapporo'},
      {id:2129, name:'Aso Stakes',date: 'Classic Year Early Aug', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kokura'},
      {id:2130, name:'Elm Stakes',date: 'Classic Year Early Aug', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Sapporo'},
      {id:2131, name:'Kanetsu Stakes',date: 'Classic Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
      {id:2132, name:'Kokura Kinen',date: 'Classic Year Early Aug', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Kokura'},
      {id:2133, name:'Leopard Stakes',date: 'Classic Year Early Aug', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Niigata'},
      {id:2134, name:'Sapporo Nikkei Open',date: 'Classic Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Long', venue: 'Sapporo'},
      {id:2135, name:'Sekiya Kinen',date: 'Classic Year Early Aug', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
      {id:2136, name:'UHB Sho',date: 'Classic Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Sapporo'},
      {id:2137, name:'BSN Sho',date: 'Classic Year Late Aug', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Niigata'},
      {id:2138, name:'Keeneland Cup',date: 'Classic Year Late Aug', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Sapporo'},
      {id:2139, name:'Kitakyushu Kinen',date: 'Classic Year Late Aug', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kokura'},
      {id:2140, name:'Kokura Nikkei Open',date: 'Classic Year Late Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kokura'},
      {id:2141, name:'NST Sho',date: 'Classic Year Late Aug', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Niigata'},
      {id:2142, name:'Sapporo Kinen',date: 'Classic Year Late Aug', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Sapporo'},
      {id:2143, name:'Toki Stakes',date: 'Classic Year Late Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2144, name:'Centaur Stakes',date: 'Classic Year Early Sep', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2145, name:'Enif Stakes',date: 'Classic Year Early Sep', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2146, name:'Keisei Hai Autumn Handicap',date: 'Classic Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2147, name:'Niigata Kinen',date: 'Classic Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Niigata'},
      {id:2148, name:'Prix Niel',date: 'Classic Year Early Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Longchamp'},
      {id:2149, name:'Radio Nippon Sho',date: 'Classic Year Early Sep', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2150, name:'Rose Stakes',date: 'Classic Year Early Sep', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2151, name:'Shion Stakes',date: 'Classic Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2152, name:'Tancho Stakes',date: 'Classic Year Early Sep', type: 'OP', terrain: 'Turf', distance: 'Long', venue: 'Sapporo'},
      {id:2153, name:'All Comers',date: 'Classic Year Late Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2154, name:'Kobe Shimbun Hai',date: 'Classic Year Late Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2155, name:'Nagatsuki Stakes',date: 'Classic Year Late Sep', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2156, name:'Port Island Stakes',date: 'Classic Year Late Sep', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2157, name:'Sirius Stakes',date: 'Classic Year Late Sep', type: 'G3', terrain: 'Dirt', distance: 'Medium', venue: 'Hanshin'},
      {id:2158, name:'Sprinters Stakes',date: 'Classic Year Late Sep', type: 'G1', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2159, name:'St. Lite Kinen',date: 'Classic Year Late Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2160, name:'Fuchu Umamusume Stakes',date: 'Classic Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2161, name:'Green Channel Cup',date: 'Classic Year Early Oct', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2162, name:'Kyoto Daishoten',date: 'Classic Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2163, name:'Mainichi Okan',date: 'Classic Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2164, name:'October Stakes',date: 'Classic Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2165, name:'Opal Stakes',date: 'Classic Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2166, name:'Shinetsu Stakes',date: 'Classic Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2167, name:'Uzumasa Stakes',date: 'Classic Year Early Oct', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
      {id:2168, name:'Brazil Cup',date: 'Classic Year Late Oct', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Tokyo'},
      {id:2169, name:'Cassiopeia Stakes',date: 'Classic Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2170, name:'Fuji Stakes',date: 'Classic Year Late Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2171, name:'Kikuka Sho',date: 'Classic Year Late Oct', type: 'G1', terrain: 'Turf', distance: 'Long', venue: 'Kyoto'},
      {id:2172, name:'Lumiere Autumn Dash',date: 'Classic Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2173, name:'Muromachi Stakes',date: 'Classic Year Late Oct', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2174, name:'Shuka Sho',date: 'Classic Year Late Oct', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2175, name:'Swan Stakes',date: 'Classic Year Late Oct', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2176, name:'Tenno Sho (Autumn)',date: 'Classic Year Late Oct', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2177, name:'Copa Republica Argentina',date: 'Classic Year Early Nov', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Tokyo'},
      {id:2178, name:'Fukushima Kinen',date: 'Classic Year Early Nov', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Fukushima'},
      {id:2179, name:'JBC Classic',date: 'Classic Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
      {id:2180, name:'JBC Ladies’ Classic',date: 'Classic Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Mile', venue: 'Ooi'},
      {id:2181, name:'JBC Sprint',date: 'Classic Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Sprint', venue: 'Ooi'},
      {id:2182, name:'Miyako Stakes',date: 'Classic Year Early Nov', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
      {id:2183, name:'Musashino Stakes',date: 'Classic Year Early Nov', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2184, name:'Oro Cup',date: 'Classic Year Early Nov', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2185, name:'Queen Elizabeth II Cup',date: 'Classic Year Early Nov', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2186, name:'Andromeda Stakes',date: 'Classic Year Late Nov', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2187, name:'Autumn Leaf Stakes',date: 'Classic Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2188, name:'Capital Stakes',date: 'Classic Year Late Nov', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2189, name:'Fukushima Minyu Cup',date: 'Classic Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Fukushima'},
      {id:2190, name:'Japan Cup',date: 'Classic Year Late Nov', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2191, name:'Keihan Hai',date: 'Classic Year Late Nov', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2192, name:'Mile Championship',date: 'Classic Year Late Nov', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2193, name:'Shimotsuki Stakes',date: 'Classic Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2194, name:'Capella Stakes',date: 'Classic Year Early Dec', type: 'G3', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2195, name:'Challenge Cup',date: 'Classic Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2196, name:'Champions Cup',date: 'Classic Year Early Dec', type: 'G1', terrain: 'Dirt', distance: 'Mile', venue: 'Chukyo'},
      {id:2197, name:'Chunichi Shimbun Hai',date: 'Classic Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Chukyo'},
      {id:2198, name:'December Stakes',date: 'Classic Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2199, name:'Lapis Lazuli Stakes',date: 'Classic Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2200, name:'Rigel Stakes',date: 'Classic Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2201, name:'Shiwasu Stakes',date: 'Classic Year Early Dec', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2202, name:'Stayers Stakes',date: 'Classic Year Early Dec', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Nakayama'},
      {id:2203, name:'Tanzanite Stakes',date: 'Classic Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2204, name:'Turquoise Stakes',date: 'Classic Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2205, name:'Arima Kinen',date: 'Classic Year Late Dec', type: 'G1', terrain: 'Turf', distance: 'Long', venue: 'Nakayama'},
      {id:2206, name:'Betelgeuse Stakes',date: 'Classic Year Late Dec', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hanshin'},
      {id:2207, name:'Galaxy Stakes',date: 'Classic Year Late Dec', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2208, name:'Hanshin Cup',date: 'Classic Year Late Dec', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2209, name:'Tokyo Daishoten',date: 'Classic Year Late Dec', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
      ],
      umamusumeRaceList_3:[
      {id:2210, name:'Aichi Hai',date: 'Senior Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Chukyo'},
      {id:2211, name:'Carbuncle Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2212, name:'January Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2213, name:'Kyoto Kimpai',date: 'Senior Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2214, name:'Manyo Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Long', venue: 'Kyoto'},
      {id:2215, name:'Nakayama Kimpai',date: 'Senior Year Early Jan', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2216, name:'New Year Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2217, name:'Nikkei Shinshun Hai',date: 'Senior Year Early Jan', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2218, name:'Pollux Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2219, name:'Yodo Tankyori Stakes',date: 'Senior Year Early Jan', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2220, name:'American JCC',date: 'Senior Year Late Jan', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2221, name:'Negishi Stakes',date: 'Senior Year Late Jan', type: 'G3', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2222, name:'Shirafuji Stakes',date: 'Senior Year Late Jan', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2223, name:'Silk Road Stakes',date: 'Senior Year Late Jan', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2224, name:'Subaru Stakes',date: 'Senior Year Late Jan', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2225, name:'Tokai Stakes',date: 'Senior Year Late Jan', type: 'G2', terrain: 'Dirt', distance: 'Mile', venue: 'Chukyo'},
      {id:2226, name:'Aldebaran Stakes',date: 'Senior Year Early Feb', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Kyoto'},
      {id:2227, name:'Kyoto Kinen',date: 'Senior Year Early Feb', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2228, name:'Rakuyo Stakes',date: 'Senior Year Early Feb', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2229, name:'Tokyo Shimbun Hai',date: 'Senior Year Early Feb', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2230, name:'Valentine Stakes',date: 'Senior Year Early Feb', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2231, name:'Yamato Stakes',date: 'Senior Year Early Feb', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2232, name:'Diamond Stakes',date: 'Senior Year Late Feb', type: 'G3', terrain: 'Turf', distance: 'Long', venue: 'Tokyo'},
      {id:2233, name:'February Stakes',date: 'Senior Year Late Feb', type: 'G1', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2234, name:'Hankyu Hai',date: 'Senior Year Late Feb', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2235, name:'Kitakyushu Tankyori Stakes',date: 'Senior Year Late Feb', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kokura'},
      {id:2236, name:'Kokura Daishoten',date: 'Senior Year Late Feb', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Kokura'},
      {id:2237, name:'Kyoto Umamusume Stakes',date: 'Senior Year Late Feb', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2238, name:'Nakayama Kinen',date: 'Senior Year Late Feb', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2239, name:'Sobu Stakes',date: 'Senior Year Late Feb', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2240, name:'Kinko Sho',date: 'Senior Year Early Mar', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Chukyo'},
      {id:2241, name:'Kochi Stakes',date: 'Senior Year Early Mar', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2242, name:'Nakayama Umamusume Stakes',date: 'Senior Year Early Mar', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2243, name:'Nigawa Stakes',date: 'Senior Year Early Mar', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Hanshin'},
      {id:2244, name:'Ocean Stakes',date: 'Senior Year Early Mar', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2245, name:'Osakajo Stakes',date: 'Senior Year Early Mar', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2246, name:'Polaris Stakes',date: 'Senior Year Early Mar', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2247, name:'Chiba Stakes',date: 'Senior Year Late Mar', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2248, name:'Hanshin Daishoten',date: 'Senior Year Late Mar', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Hanshin'},
      {id:2249, name:'March Stakes',date: 'Senior Year Late Mar', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2250, name:'Nikkei Sho',date: 'Senior Year Late Mar', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Nakayama'},
      {id:2251, name:'Osaka Hai',date: 'Senior Year Late Mar', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2252, name:'Rokko Stakes',date: 'Senior Year Late Mar', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2253, name:'Takamatsunomiya Kinen',date: 'Senior Year Late Mar', type: 'G1', terrain: 'Turf', distance: 'Sprint', venue: 'Chukyo'},
      {id:2254, name:'Antares Stakes',date: 'Senior Year Early Apr', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Hanshin'},
      {id:2255, name:'Azumakofuji Stakes',date: 'Senior Year Early Apr', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Fukushima'},
      {id:2256, name:'Coral Stakes',date: 'Senior Year Early Apr', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2257, name:'Fukushima Mimpo Hai',date: 'Senior Year Early Apr', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Fukushima'},
      {id:2258, name:'Hanshin Umamusume Stakes',date: 'Senior Year Early Apr', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2259, name:'Keiyo Stakes',date: 'Senior Year Early Apr', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2260, name:'Lord Derby Challenge Trophy',date: 'Senior Year Early Apr', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2261, name:'Shunrai Stakes',date: 'Senior Year Early Apr', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2262, name:'Fukushima Umamusume Stakes',date: 'Senior Year Late Apr', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Fukushima'},
      {id:2263, name:'Milers Cup',date: 'Senior Year Late Apr', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2264, name:'Oasis Stakes',date: 'Senior Year Late Apr', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2265, name:'Tenno Sho (Spring)',date: 'Senior Year Late Apr', type: 'G1', terrain: 'Turf', distance: 'Long', venue: 'Kyoto'},
      {id:2266, name:'Tennozan Stakes',date: 'Senior Year Late Apr', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2267, name:'Brilliant Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Tokyo'},
      {id:2268, name:'Keio Hai Spring Cup',date: 'Senior Year Early May', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2269, name:'Kurama Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2270, name:'Metropolitan Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2271, name:'Miyakooji Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2272, name:'Niigata Daishoten',date: 'Senior Year Early May', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Niigata'},
      {id:2273, name:'Ritto Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2274, name:'Tanigawadake Stakes',date: 'Senior Year Early May', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
      {id:2275, name:'Victoria Mile',date: 'Senior Year Early May', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2276, name:'Azuchijo Stakes',date: 'Senior Year Late May', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2277, name:'Heian Stakes',date: 'Senior Year Late May', type: 'G3', terrain: 'Dirt', distance: 'Medium', venue: 'Kyoto'},
      {id:2278, name:'Idaten Stakes',date: 'Senior Year Late May', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2279, name:'Keyaki Stakes',date: 'Senior Year Late May', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2280, name:'May Stakes',date: 'Senior Year Late May', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2281, name:'Meguro Kinen',date: 'Senior Year Late May', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Tokyo'},
      {id:2282, name:'Epsom Cup',date: 'Senior Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2283, name:'Mermaid Stakes',date: 'Senior Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2284, name:'Naruo Kinen',date: 'Senior Year Early Jun', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2285, name:'Sleipnir Stakes',date: 'Senior Year Early Jun', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Tokyo'},
      {id:2286, name:'Tempozan Stakes',date: 'Senior Year Early Jun', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2287, name:'Yasuda Kinen',date: 'Senior Year Early Jun', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2288, name:'Akhalteke Stakes',date: 'Senior Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2289, name:'Hakodate Sprint Stakes',date: 'Senior Year Late Jun', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Hakodate'},
      {id:2290, name:'Onuma Stakes',date: 'Senior Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hakodate'},
      {id:2291, name:'Paradise Stakes',date: 'Senior Year Late Jun', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2292, name:'Sannomiya Stakes',date: 'Senior Year Late Jun', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hanshin'},
      {id:2293, name:'Takarazuka Kinen',date: 'Senior Year Late Jun', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2294, name:'Teio Sho',date: 'Senior Year Late Jun', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
      {id:2295, name:'Yonago Stakes',date: 'Senior Year Late Jun', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2296, name:'CBC Sho',date: 'Senior Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Chukyo'},
      {id:2297, name:'Hakodate Kinen',date: 'Senior Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hakodate'},
      {id:2298, name:'Marine Stakes',date: 'Senior Year Early Jul', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hakodate'},
      {id:2299, name:'Meitetsu Hai',date: 'Senior Year Early Jul', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Chukyo'},
      {id:2300, name:'Procyon Stakes',date: 'Senior Year Early Jul', type: 'G3', terrain: 'Dirt', distance: 'Sprint', venue: 'Chukyo'},
      {id:2301, name:'Tanabata Sho',date: 'Senior Year Early Jul', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Fukushima'},
      {id:2302, name:'Tomoe Sho',date: 'Senior Year Early Jul', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hakodate'},
      {id:2303, name:'Chukyo Kinen',date: 'Senior Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Chukyo'},
      {id:2304, name:'Fukushima TV Open',date: 'Senior Year Late Jul', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Fukushima'},
      {id:2305, name:'Ibis Summer Dash',date: 'Senior Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2306, name:'Queen Stakes',date: 'Senior Year Late Jul', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Sapporo'},
      {id:2307, name:'Aso Stakes',date: 'Senior Year Early Aug', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kokura'},
      {id:2308, name:'Elm Stakes',date: 'Senior Year Early Aug', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Sapporo'},
      {id:2309, name:'Kanetsu Stakes',date: 'Senior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
      {id:2310, name:'Kokura Kinen',date: 'Senior Year Early Aug', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Kokura'},
      {id:2311, name:'Sapporo Nikkei Open',date: 'Senior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Long', venue: 'Sapporo'},
      {id:2312, name:'Sekiya Kinen',date: 'Senior Year Early Aug', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Niigata'},
      {id:2313, name:'UHB Sho',date: 'Senior Year Early Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Sapporo'},
      {id:2314, name:'BSN Sho',date: 'Senior Year Late Aug', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Niigata'},
      {id:2315, name:'Keeneland Cup',date: 'Senior Year Late Aug', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Sapporo'},
      {id:2316, name:'Kitakyushu Kinen',date: 'Senior Year Late Aug', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kokura'},
      {id:2317, name:'Kokura Nikkei Open',date: 'Senior Year Late Aug', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kokura'},
      {id:2318, name:'NST Sho',date: 'Senior Year Late Aug', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Niigata'},
      {id:2319, name:'Sapporo Kinen',date: 'Senior Year Late Aug', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Sapporo'},
      {id:2320, name:'Toki Stakes',date: 'Senior Year Late Aug', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2321, name:'Centaur Stakes',date: 'Senior Year Early Sep', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2322, name:'Enif Stakes',date: 'Senior Year Early Sep', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2323, name:'Keisei Hai Autumn Handicap',date: 'Senior Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2324, name:'Niigata Kinen',date: 'Senior Year Early Sep', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Niigata'},
      {id:2325, name:'Prix Foy',date: 'Senior Year Early Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Longchamp'},
      {id:2326, name:'Radio Nippon Sho',date: 'Senior Year Early Sep', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2327, name:'Tancho Stakes',date: 'Senior Year Early Sep', type: 'OP', terrain: 'Turf', distance: 'Long', venue: 'Sapporo'},
      {id:2328, name:'All Comers',date: 'Senior Year Late Sep', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Nakayama'},
      {id:2329, name:'Nagatsuki Stakes',date: 'Senior Year Late Sep', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2330, name:'Port Island Stakes',date: 'Senior Year Late Sep', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2331, name:'Sirius Stakes',date: 'Senior Year Late Sep', type: 'G3', terrain: 'Dirt', distance: 'Medium', venue: 'Hanshin'},
      {id:2332, name:'Sprinters Stakes',date: 'Senior Year Late Sep', type: 'G1', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2333, name:'Fuchu Umamusume Stakes',date: 'Senior Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2334, name:'Green Channel Cup',date: 'Senior Year Early Oct', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2335, name:'Kyoto Daishoten',date: 'Senior Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2336, name:'Mainichi Okan',date: 'Senior Year Early Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2337, name:'October Stakes',date: 'Senior Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2338, name:'Opal Stakes',date: 'Senior Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2339, name:'Shinetsu Stakes',date: 'Senior Year Early Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2340, name:'Uzumasa Stakes',date: 'Senior Year Early Oct', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
      {id:2341, name:'Brazil Cup',date: 'Senior Year Late Oct', type: 'OP', terrain: 'Dirt', distance: 'Medium', venue: 'Tokyo'},
      {id:2342, name:'Cassiopeia Stakes',date: 'Senior Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2343, name:'Fuji Stakes',date: 'Senior Year Late Oct', type: 'G2', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2344, name:'Lumiere Autumn Dash',date: 'Senior Year Late Oct', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Niigata'},
      {id:2345, name:'Muromachi Stakes',date: 'Senior Year Late Oct', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2346, name:'Swan Stakes',date: 'Senior Year Late Oct', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2347, name:'Tenno Sho (Autumn)',date: 'Senior Year Late Oct', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2348, name:'Copa Republica Argentina',date: 'Senior Year Early Nov', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Tokyo'},
      {id:2349, name:'Fukushima Kinen',date: 'Senior Year Early Nov', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Fukushima'},
      {id:2350, name:'JBC Classic',date: 'Senior Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
      {id:2351, name:'JBC Ladies’ Classic',date: 'Senior Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Mile', venue: 'Ooi'},
      {id:2352, name:'JBC Sprint',date: 'Senior Year Early Nov', type: 'G1', terrain: 'Dirt', distance: 'Sprint', venue: 'Ooi'},
      {id:2353, name:'Miyako Stakes',date: 'Senior Year Early Nov', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Kyoto'},
      {id:2354, name:'Musashino Stakes',date: 'Senior Year Early Nov', type: 'G3', terrain: 'Dirt', distance: 'Mile', venue: 'Tokyo'},
      {id:2355, name:'Oro Cup',date: 'Senior Year Early Nov', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Tokyo'},
      {id:2356, name:'Queen Elizabeth II Cup',date: 'Senior Year Early Nov', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2357, name:'Andromeda Stakes',date: 'Senior Year Late Nov', type: 'OP', terrain: 'Turf', distance: 'Medium', venue: 'Kyoto'},
      {id:2358, name:'Autumn Leaf Stakes',date: 'Senior Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Kyoto'},
      {id:2359, name:'Capital Stakes',date: 'Senior Year Late Nov', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Tokyo'},
      {id:2360, name:'Fukushima Minyu Cup',date: 'Senior Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Fukushima'},
      {id:2361, name:'Japan Cup',date: 'Senior Year Late Nov', type: 'G1', terrain: 'Turf', distance: 'Medium', venue: 'Tokyo'},
      {id:2362, name:'Keihan Hai',date: 'Senior Year Late Nov', type: 'G3', terrain: 'Turf', distance: 'Sprint', venue: 'Kyoto'},
      {id:2363, name:'Mile Championship',date: 'Senior Year Late Nov', type: 'G1', terrain: 'Turf', distance: 'Mile', venue: 'Kyoto'},
      {id:2364, name:'Shimotsuki Stakes',date: 'Senior Year Late Nov', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Tokyo'},
      {id:2365, name:'Capella Stakes',date: 'Senior Year Early Dec', type: 'G3', terrain: 'Dirt', distance: 'Sprint', venue: 'Nakayama'},
      {id:2366, name:'Challenge Cup',date: 'Senior Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Hanshin'},
      {id:2367, name:'Champions Cup',date: 'Senior Year Early Dec', type: 'G1', terrain: 'Dirt', distance: 'Mile', venue: 'Chukyo'},
      {id:2368, name:'Chunichi Shimbun Hai',date: 'Senior Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Medium', venue: 'Chukyo'},
      {id:2369, name:'December Stakes',date: 'Senior Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2370, name:'Lapis Lazuli Stakes',date: 'Senior Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Nakayama'},
      {id:2371, name:'Rigel Stakes',date: 'Senior Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Mile', venue: 'Hanshin'},
      {id:2372, name:'Shiwasu Stakes',date: 'Senior Year Early Dec', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Nakayama'},
      {id:2373, name:'Stayers Stakes',date: 'Senior Year Early Dec', type: 'G2', terrain: 'Turf', distance: 'Long', venue: 'Nakayama'},
      {id:2374, name:'Tanzanite Stakes',date: 'Senior Year Early Dec', type: 'OP', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2375, name:'Turquoise Stakes',date: 'Senior Year Early Dec', type: 'G3', terrain: 'Turf', distance: 'Mile', venue: 'Nakayama'},
      {id:2376, name:'Arima Kinen',date: 'Senior Year Late Dec', type: 'G1', terrain: 'Turf', distance: 'Long', venue: 'Nakayama'},
      {id:2377, name:'Betelgeuse Stakes',date: 'Senior Year Late Dec', type: 'OP', terrain: 'Dirt', distance: 'Mile', venue: 'Hanshin'},
      {id:2378, name:'Galaxy Stakes',date: 'Senior Year Late Dec', type: 'OP', terrain: 'Dirt', distance: 'Sprint', venue: 'Hanshin'},
      {id:2379, name:'Hanshin Cup',date: 'Senior Year Late Dec', type: 'G2', terrain: 'Turf', distance: 'Sprint', venue: 'Hanshin'},
      {id:2380, name:'Tokyo Daishoten',date: 'Senior Year Late Dec', type: 'G1', terrain: 'Dirt', distance: 'Medium', venue: 'Ooi'},
    ],
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
      
      // Skill data from const.py
      skillPriority0: [
        'Corner Acceleration ◯', 'Corner Adept ◯', 'Slipstream', 'Tail Held High', 
        'Straightaway Spurt', 'Ramp Up', 'Inside Scoop', 'Passing Pro', 'Homestretch Haste',
        'Fast-Paced', 'Outer Swell', 'Sprinting Gear', 'Slick Surge', 'Corner Recovery ◯',
        'Hydrate', 'After-School Stroll', 'Clean Heart', 'Dominator', 'All-Seeing Eyes', 'Mystifying Murmur'
      ],
      skillPriority1: [
        'Acceleration', 'Focus', 'Go with the Flow', 'I Can See Right Through You', 
        'Nimble Navigator', 'Straightaway Recovery', 'Deep Breaths', 'Preferred Position',
        'Groundwork', 'Up-Tempo', 'Unyielding Spirit', 'Pressure', 'Strategist', 'Triple 7s',
        'Shake It Out', 'Intimidate', 'Stamina Eater', 'Intense Gaze', 'Speed Star',
        'Staggering Lead', 'Blinding Flash', 'Restless', 'Trackblazer', 'Meticulous Measures',
        'Keeping the Lead', 'Leader\'s Pride', 'Wait-and-See', 'A Small Breather'
      ],
      skillPriority2: [
        'Levelheaded', 'Stop Right There!', 'Super Lucky Seven', 'Maverick ◯', 'Sympathy',
        'Long Shot ◯', 'Inner Post Proficiency ◯', 'Outer Post Proficiency ◯', 'Right-Handed ◯',
        'Left-Handed ◯', 'Firm Conditions ◯', 'Wet Conditions ◯', 'Standard Distance ◯', 
        'Non-Standard Distance ◯', 'Competitive Spirit ◯', 'Target in Sight ◯', 'Lone Wolf'
      ],
      selectedSkills: [],
      blacklistedSkills: [],
    }
  },
  computed: {
    filteredRaces_1() {
      return this.umamusumeRaceList_1.filter(race => {
        const matchesSearch = !this.raceSearch || 
          race.name.toLowerCase().includes(this.raceSearch.toLowerCase()) ||
          race.date.toLowerCase().includes(this.raceSearch.toLowerCase());
        const matchesType = 
          (race.type === 'G1' && this.showGI) ||
          (race.type === 'G2' && this.showGII) ||
          (race.type === 'G3' && this.showGIII) ||
          (race.type === 'OP' && this.showOP) ||
          (race.type === 'PRE-OP' && this.showPREOP);
        const matchesTerrain = 
          (race.terrain === 'Turf' && this.showTurf) ||
          (race.terrain === 'Dirt' && this.showDirt);
        const matchesDistance = 
          (race.distance === 'Sprint' && this.showSprint) ||
          (race.distance === 'Mile' && this.showMile) ||
          (race.distance === 'Medium' && this.showMedium) ||
          (race.distance === 'Long' && this.showLong);
        
        // Character filter logic
        let matchesCharacter = true;
        if (this.selectedCharacter) {
          const character = this.characterList.find(c => c.name === this.selectedCharacter);
          if (character) {
            // Check if race matches character's aptitude (terrain and distance)
            const matchesAptitude = race.terrain === character.terrain && race.distance === character.distance;
            
            // Check if race date is within character's training periods
            const characterPeriods = this.characterTrainingPeriods[this.selectedCharacter];
            const matchesTrainingPeriod = characterPeriods && 
              characterPeriods['Junior Year'] && 
              characterPeriods['Junior Year'].includes(race.date);
            
            matchesCharacter = matchesAptitude && matchesTrainingPeriod;
          }
        }
        
        return matchesSearch && matchesType && matchesTerrain && matchesDistance && matchesCharacter;
      });
    },
    filteredRaces_2() {
      return this.umamusumeRaceList_2.filter(race => {
        const matchesSearch = !this.raceSearch || 
          race.name.toLowerCase().includes(this.raceSearch.toLowerCase()) ||
          race.date.toLowerCase().includes(this.raceSearch.toLowerCase());
        const matchesType = 
          (race.type === 'G1' && this.showGI) ||
          (race.type === 'G2' && this.showGII) ||
          (race.type === 'G3' && this.showGIII) ||
          (race.type === 'OP' && this.showOP) ||
          (race.type === 'PRE-OP' && this.showPREOP);
        const matchesTerrain = 
          (race.terrain === 'Turf' && this.showTurf) ||
          (race.terrain === 'Dirt' && this.showDirt);
        const matchesDistance = 
          (race.distance === 'Sprint' && this.showSprint) ||
          (race.distance === 'Mile' && this.showMile) ||
          (race.distance === 'Medium' && this.showMedium) ||
          (race.distance === 'Long' && this.showLong);
        
        // Character filter logic
        let matchesCharacter = true;
        if (this.selectedCharacter) {
          const character = this.characterList.find(c => c.name === this.selectedCharacter);
          if (character) {
            // Check if race matches character's aptitude (terrain and distance)
            const matchesAptitude = race.terrain === character.terrain && race.distance === character.distance;
            
            // Check if race date is within character's training periods
            const characterPeriods = this.characterTrainingPeriods[this.selectedCharacter];
            const matchesTrainingPeriod = characterPeriods && 
              characterPeriods['Classic Year'] && 
              characterPeriods['Classic Year'].includes(race.date);
            
            matchesCharacter = matchesAptitude && matchesTrainingPeriod;
          }
        }
        
        return matchesSearch && matchesType && matchesTerrain && matchesDistance && matchesCharacter;
      });
    },
    filteredRaces_3() {
      return this.umamusumeRaceList_3.filter(race => {
        const matchesSearch = !this.raceSearch || 
          race.name.toLowerCase().includes(this.raceSearch.toLowerCase()) ||
          race.date.toLowerCase().includes(this.raceSearch.toLowerCase());
        const matchesType = 
          (race.type === 'G1' && this.showGI) ||
          (race.type === 'G2' && this.showGII) ||
          (race.type === 'G3' && this.showGIII) ||
          (race.type === 'OP' && this.showOP) ||
          (race.type === 'PRE-OP' && this.showPREOP);
        const matchesTerrain = 
          (race.terrain === 'Turf' && this.showTurf) ||
          (race.terrain === 'Dirt' && this.showDirt);
        const matchesDistance = 
          (race.distance === 'Sprint' && this.showSprint) ||
          (race.distance === 'Mile' && this.showMile) ||
          (race.distance === 'Medium' && this.showMedium) ||
          (race.distance === 'Long' && this.showLong);
        
        // Character filter logic
        let matchesCharacter = true;
        if (this.selectedCharacter) {
          const character = this.characterList.find(c => c.name === this.selectedCharacter);
          if (character) {
            // Check if race matches character's aptitude (terrain and distance)
            const matchesAptitude = race.terrain === character.terrain && race.distance === character.distance;
            
            // Check if race date is within character's training periods
            const characterPeriods = this.characterTrainingPeriods[this.selectedCharacter];
            const matchesTrainingPeriod = characterPeriods && 
              characterPeriods['Senior Year'] && 
              characterPeriods['Senior Year'].includes(race.date);
            
            matchesCharacter = matchesAptitude && matchesTrainingPeriod;
          }
        }
        
        return matchesSearch && matchesType && matchesTerrain && matchesDistance && matchesCharacter;
      });
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
    // Quick selection methods
    selectAllGI: function() {
      const allGIRaces = [
        ...this.umamusumeRaceList_1.filter(race => race.type === 'GI'),
        ...this.umamusumeRaceList_2.filter(race => race.type === 'GI'),
        ...this.umamusumeRaceList_3.filter(race => race.type === 'GI')
      ];
      allGIRaces.forEach(race => {
        if (!this.extraRace.includes(race.id)) {
          this.extraRace.push(race.id);
        }
      });
    },
    selectAllGII: function() {
      const allGIIRaces = [
        ...this.umamusumeRaceList_1.filter(race => race.type === 'GII'),
        ...this.umamusumeRaceList_2.filter(race => race.type === 'GII'),
        ...this.umamusumeRaceList_3.filter(race => race.type === 'GII')
      ];
      allGIIRaces.forEach(race => {
        if (!this.extraRace.includes(race.id)) {
          this.extraRace.push(race.id);
        }
      });
    },
    selectAllGIII: function() {
      const allGIIIRaces = [
        ...this.umamusumeRaceList_1.filter(race => race.type === 'GIII'),
        ...this.umamusumeRaceList_2.filter(race => race.type === 'GIII'),
        ...this.umamusumeRaceList_3.filter(race => race.type === 'GIII')
      ];
      allGIIIRaces.forEach(race => {
        if (!this.extraRace.includes(race.id)) {
          this.extraRace.push(race.id);
        }
      });
    },
    clearAllRaces: function() {
      this.extraRace = [];
    },
    onCharacterChange: function() {
      // Reset race selection when character changes
      this.extraRace = [];
    },
    toggleRace: function(raceId) {
      const index = this.extraRace.indexOf(raceId);
      if (index > -1) {
        this.extraRace.splice(index, 1);
      } else {
        this.extraRace.push(raceId);
      }
    },
    toggleSkill: function(skillName) {
      const index = this.selectedSkills.indexOf(skillName);
      if (index > -1) {
        this.selectedSkills.splice(index, 1);
      } else {
        this.selectedSkills.push(skillName);
      }
    },
    toggleBlacklistSkill: function(skillName) {
      const index = this.blacklistedSkills.indexOf(skillName);
      if (index > -1) {
        this.blacklistedSkills.splice(index, 1);
      } else {
        this.blacklistedSkills.push(skillName);
      }
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

/* Race Toggle Styles */
.race-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  padding: 8px;
}

.race-toggle {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.race-toggle:hover {
  background: #e9ecef;
  border-color: #007bff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.15);
}

.race-toggle.selected {
  background: #007bff;
  border-color: #0056b3;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

.race-toggle.selected:hover {
  background: #0056b3;
  border-color: #004085;
}

.race-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.race-name {
  font-weight: 600;
  font-size: 14px;
  line-height: 1.3;
  margin-bottom: 4px;
}

.race-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 4px;
}

.race-badges .badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 12px;
}

.race-details {
  font-size: 11px;
  opacity: 0.8;
  line-height: 1.2;
}

.race-toggle.selected .race-details {
  opacity: 0.9;
}

/* Skill Toggle Styles */
.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
  padding: 8px;
}

.skill-toggle {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.skill-toggle:hover {
  background: #e9ecef;
  border-color: #007bff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.15);
}

.skill-toggle.selected {
  background: #007bff;
  border-color: #0056b3;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

.skill-toggle.selected:hover {
  background: #0056b3;
  border-color: #004085;
}

.skill-toggle.blacklist-toggle {
  border-color: #dc3545;
}

.skill-toggle.blacklist-toggle:hover {
  border-color: #c82333;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.15);
}

.skill-toggle.blacklist-toggle.selected {
  background: #dc3545;
  border-color: #c82333;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);
}

.skill-toggle.blacklist-toggle.selected:hover {
  background: #c82333;
  border-color: #a71e2a;
}

.skill-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.skill-name {
  font-weight: 600;
  font-size: 12px;
  line-height: 1.2;
  margin-bottom: 2px;
}

.skill-priority {
  font-size: 10px;
  opacity: 0.8;
  line-height: 1.1;
}

.form-label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #495057;
}
</style>