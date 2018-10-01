import React from 'react';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';

import UserList from './user-list';

const users = [
  {
    active: true,
    email: 'email1@foo.com',
    id: 1,
    username: 'username_1',
  },
  {
    active: true,
    email: 'joes_email@foo.com',
    id: 2,
    username: 'joes_username',
  },
];

test('UserList renders properly', () => {
  const wrapper = shallow(<UserList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  const expected = [`${users[0].username}`,'(',`${users[0].email}`, ')'];
  const results = element.get(0).props.children;
  expect(JSON.stringify(results)).toBe(JSON.stringify(expected));
});

test('UserList renders snapshot properly', () => {
  const tree = renderer.create(<UserList users={users}/>);
  expect(tree).toMatchSnapshot();
});
