<template>
  <div class="hello ">
    <section class="hero is-info ">
      <div class="hero-body">
        <h3 class="title">Light-logger</h3>
        <p class="subtitle">
          A light-weight log visualizer
        </p>
      </div>


      <div class="has-text-centered pb-2">
          <button class="button is-small"
              @click="fetchLogs">Show today's logs
          </button>

          <div class="has-text-right mr-3">
            <input type="date" v-model="start_date" class="p-1" name="Start date">

            &nbsp;
            <input type="date" v-model="end_date" class="p-1" name="End date">
            &nbsp;
            <button class="button is-primary is-small" @click="fetchLogs">Search</button>

            &nbsp;
            <button class="button is-white is-small"
                @click="resetFilters">Reset
            </button>
          </div>

      </div>

    </section>

    <section class="section log-section" id="log">
       <div v-if="logs.length>0 && is_data_ready" class="has-text-left">
          <p>Logs for -
              <u><b>{{new Date(start_date).toDateString()}} - {{new Date(end_date).toDateString()}}</b></u>
              (Latest first)
          </p>
          <hr>
          <div  v-for="(log,idx) in logs" :key="idx" >
              <p class="pb-1">{{log}}</p>
          </div>
      </div>

      <div v-else>
        No records yet
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
        is_data_ready:false
      }
    },

  created: function() {
      console.log("Starting connection to WebSocket Server")
      this.connection = new WebSocket("ws://127.0.0.1:8001/ws")

      let self = this
      self.connection.onmessage = function(event) {
          // const resp = JSON.parse(event.data)
          // self.page_number = resp.page_no
          // self.per_page = resp.per_page

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
      window.addEventListener('scroll', this.loadMore)

      // let element = document.getElementById('log')
      // element.addEventListener('scroll', function(event)
      // {
      //     let element = event.target;
      //     if (element.scrollHeight - element.scrollTop === element.clientHeight)
      //     {
      //         // this.loadMore()
      //     }
      // });
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
          let data = {
              start_date: this.formattedDate(this.start_date),
              end_date: this.formattedDate(this.end_date),
              per_page:50,
          }
          this.connection.send(JSON.stringify(data))
      },

      loadMore: function (){
          if (this.is_data_ready){
              console.log('******')
              let data = {
                  start_date: this.formattedDate(this.start_date),
                  end_date: this.formattedDate(this.end_date),
                  per_page:50,
              }
              this.connection.send(JSON.stringify(data))
          }
      },

      resetFilters: function (){
          this.start_date=new Date()
          this.end_date = new Date()
          this.logs=[]
          this.is_data_ready = false
      },

  },

  unmounted () {
      // let element = document.getElementById('log')
      // element.removeEventListener('scroll', this.loadMore);
      window.removeEventListener('scroll', this.loadMore)
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
#log{
  overflow-y: scroll;
  height: 600px
}

</style>
