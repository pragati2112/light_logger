<template>
  <div class="hello ">
    <section class="hero is-link ">
      <div class="hero-body">
        <h3 class="title">Light-logger</h3>
        <p class="subtitle">
          A light-weight log visualizer
        </p>
      </div>
    </section>

    <section class="section" id="log" ref="logContainer">
      <div class="box grow">
        <w-grid columns="2" gap="3" class="wrapper">
         <w-flex justify-start gap="3">
            <w-input class="pa1" v-model="filePath"
                     label="Paste the log file path"
                     style="max-width: 240px">
            </w-input>

            <w-select :items="logTypes" class="pa1"
                      v-model="selectedLogType"
                      inner-icon-left="mdi mdi-star"
                      label="Select log type"
                      outline style="max-width: 240px">
            </w-select>

           <w-button class="pa1 mt2" @click="processingLogFile()">Submit</w-button>
          </w-flex>

        <w-flex justify-end gap="3">
            <w-button @click="fetchLogs" outline class="mt2">Show today's logs</w-button>
            <w-input type="date" v-model="start_date" outline style="max-width: 200px"
                     placeholder="Start date" label="Start date">
            </w-input>
            <w-input type="date" v-model="end_date" outline style="max-width: 200px"
                     placeholder="End date" label="End date">
            </w-input>
            <w-button @click="fetchLogs" class="mt2">Search</w-button>
            <w-button @click="resetFilters" outline class="mt2" color="white">Reset</w-button>
          </w-flex>
        </w-grid>

      </div>

      <div v-if="logs.length>0 && is_data_ready"  class="has-text-left">
          <p>Logs for -
              <u><b>{{new Date(start_date).toDateString()}} - {{new Date(end_date).toDateString()}}</b></u>
              (Latest first)
          </p>
          <hr>
          <div  v-for="(log,idx) in logs" :key="idx" >
              <p class="pb-1">{{log}}</p>
          </div>
       </div>

      <div v-else-if="request_sent" class="mt-1">
          <p>No records found in <b>{{new Date(start_date).toDateString()}} -
            {{new Date(end_date).toDateString()}}</b></p>
      </div>

    </section>
  </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },

  data() {
      return {
        message: 'Hello light logger!',
        connection: null,
        per_page:50,
        logs:[],
        start_date:new Date(),
        end_date:new Date(),
        is_data_ready:false,
        request_sent:false,
        selectedLogType:[],
        filePath:'',
        logTypes:[
          { label: 'Item 1' , value: 1},
          { label: 'Item 2', value: 2 },
          { label: 'Item 3', value: 3 }
        ]
      }
    },

  created: function() {
      console.log("Starting connection to WebSocket Server")
      this.connection = new WebSocket("ws://127.0.0.1:8001/ws")

      let self = this
      self.connection.onmessage = function(event) {
          if(event){
              self.logs.push(event.data)
              self.is_data_ready = true
          }
      }

      self.connection.onopen = function(event) {
        console.log(event)
        console.log("Successfully connected to the echo websocket server...")
      }
  },

  mounted(){
      // const doc = getCurrentInstance()
      let self = this
      let element = self.$refs.logContainer
      element.addEventListener('wheel', self.loadMore);
  },

  methods:{
      formattedDate:function(d){
          let date = new Date(d)
          let year = date.toLocaleDateString("default", { year: "numeric" });
          let month = date.toLocaleDateString("default", { month: "2-digit" });
          let day = date.toLocaleDateString("default", { day: "2-digit" });
          return year + "-" + month + "-" + day
      },

      fetchLogs: function (){
          this.logs=[]
          let data = {
              start_date: this.formattedDate(this.$data.start_date),
              end_date: this.formattedDate(this.$data.end_date),
              per_page:50,
          }
          this.connection.send(JSON.stringify(data))
          this.$data.request_sent = true
      },

      loadMore: function (){
          let element = document.getElementById('log')
          if (element.scrollHeight - element.scrollTop === element.clientHeight){
            if (this.is_data_ready){
              let data = {
                  start_date: this.formattedDate(this.$data.start_date),
                  end_date: this.formattedDate(this.$data.end_date),
                  per_page:50,
              }
              this.connection.send(JSON.stringify(data))
            }
          }
      },

      resetFilters: function (){
          this.start_date=new Date()
          this.end_date = new Date()
          this.logs=[]
          this.is_data_ready = false
          this.$data.request_sent = false
      },

      processingLogFile: function (){
        if (this.$data.filePath === '' || this.$data.selectedLogType===''){
          this.$waveui.notify("Please fill the required fields", 'error')
        }
        let data = {
          file_path: this.$data.filePath,
          log_type: this.selectedLogType
        }
        this.$waveui.notify("We are processing the log file. In some time you'll be able to access it.")
      }

  },

  unmounted () {
      let element = document.getElementById('log')
      element.removeEventListener('wheel', this.loadMore);
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
a {
  color: #42b983;
}
#log{
  overflow-y: scroll;
  height: 600px
}
.w-select__menu {
  margin: 0;
  max-height: 300px;
  overflow: auto;
  background-color: rgba(33, 37, 43, 1) !important;
  border: 1px solid rgba(0,0,0,.15);
  border-radius: 3px;
}
</style>
