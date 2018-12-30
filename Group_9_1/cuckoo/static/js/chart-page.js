//Bar chart
new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: ['惊悚', '冒险', '剧情', '动作', '传记', '喜剧', '动画', '家庭', '爱情', '科幻', '灾难', '音乐',
                  '奇幻', '悬疑', '黑色电影', '武侠', '战争', '古装', '历史', '运动', '恐怖', '歌舞', '犯罪', '纪录片',
                  '戏曲', '短片', '西部'],
      datasets: [
        {
          label: "票房",
          backgroundColor: ['#5c2223', '#ef3473', '#894e54', '#681752', '#8b2671', '#806d9e',
                         '#1c2938', '#144a74', '#126e82', '#619ac3', '#248067', '#1a6840', '#5bae23',
                         '#b78d12', '#f6c430', '#db8540', '#964d22', '#ab372f', '#ac1f18', '#f1908c',
                         '#47484c', '#2d2e36', '#5d3f51', '#495c69', '#74787a', '#869d9d', '#497568'],
          data: [2478,5267,734,784,433]
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: '2015年各类型电影票房累计'
      }
    }
});


//Doughnut Chart1
new Chart(document.getElementById("doughnut-chart1"), {
    type: 'doughnut',
    data: {
      labels: ['惊悚', '冒险', '剧情', '动作', '传记', '喜剧', '动画', '家庭', '爱情', '科幻', '灾难', '音乐',
                  '奇幻', '悬疑', '黑色电影', '武侠', '战争', '古装', '历史', '运动', '恐怖', '歌舞', '犯罪', '纪录片',
                  '戏曲', '短片', '西部'],
      datasets: [
        {
          label: "票房",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: [2478,5267,734,784,433]
        }
      ]
    },
    options: {
        title: {
            display: true,
            text: '2015年各类型电影票房占比'
        }
    },
    // Line
});


