const list = [[1,2],[3,4],[1,4]];
const sublist = [1,4];

if (list.some(item => JSON.stringify(item) === JSON.stringify(sublist))) {
  console.log('sublist exists in list');
} else {
  console.log('sublist does not exist in list');
}