const oldList = [
  [
      "9670f5337a524d17b5a9354d7df6558a",
      "9670f5337a524d17b5a9354d7df6558a"
  ],
  [
      "Myproject",
      "a"
  ],
  [
      "Myproject",
      "b"
  ],
  [
      "Youproject",
      "c"
  ],
  [
      "ooo",
      "d"
  ],
  [
      "默认项目",
      "e"
  ]
]

const newList = [
[
    "Myproject",
    "a"
],
[
    "ooo",
    "d"
],
[
    "默认项目",
    "e"
]
]

diff_item_list=[]
oldList.forEach(element => {
  if(! newList.some(item => JSON.stringify(item) === JSON.stringify(element))){
      diff_item_list.push(element)
  }
});
console.log(diff_item_list)