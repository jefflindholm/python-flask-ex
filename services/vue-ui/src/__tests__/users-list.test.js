import { mount } from '@vue/test-utils';
import { createRenderer } from 'vue-server-renderer'
import UsersList from '../components/users-list';

const users = [
  { active: true, email: 'jeff@lindholm.org', id: 1, username: 'jeff' },
  { active: true, email: 'iryna@lindholm.org', id: 2, username: 'iryna' },
];

test('UsersList renders properly', () => {
  const vm = mount(UsersList, { propsData: { users }});
  const h4 = vm.findAll('h4');
  expect(h4).toHaveLength(users.length);
  expect(h4.at(0).text()).toContain('jeff');
  ['card', 'card-body', 'bg-light'].forEach(c => expect(h4.at(0).classes()).toContain(c) );
});

test('UsersList renders correct snapshot', () => {
  const renderer = createRenderer();
  const vm = mount(UsersList, { propsData: { users }});
  renderer.renderToString(vm.vm, (err, str) => {
    if (err) throw new Error(err);
    expect(str).toMatchSnapshot();
  });
})
