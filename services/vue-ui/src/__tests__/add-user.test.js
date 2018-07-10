import { mount } from '@vue/test-utils';
import { createRenderer } from 'vue-server-renderer'
import AddUser from '../components/add-user';

test('UsersList renders properly', () => {
  const vm = mount(AddUser);
  const inputs = vm.findAll('input');
  expect(inputs).toHaveLength(3);
  expect(inputs.at(0).attributes().name).toBe('username');
  expect(inputs.at(1).attributes().name).toBe('email');
  expect(inputs.at(2).attributes().type).toBe('submit');
});


test('UsersList renders correct snapshot', () => {
  const renderer = createRenderer();
  const vm = mount(AddUser);
  renderer.renderToString(vm.vm, (err, str) => {
    if (err) throw new Error(err);
    expect(str).toMatchSnapshot();
  });
});
