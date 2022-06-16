async created() {
    // 필요 시 데이터 가져오는 로직
    // 차트생성에 사용할 옵션과 데이터가 결정될 것이다.
  },
  async mounted() {
    // 마운트 된 두 ref에 접근할 수 있으므로 마운트 뒤 차트를 그린다.
    await this.drawChart();
  },
  methods: {
    drawChart() {
      const chartCtx = this.$refs.lineChart.getContext("2d");
      console.log(chartCtx, "chartCtx?");
      // context와 Chart.js객체, 데이터가 결정됐으니  그리기만 하면된다.
    },
  }