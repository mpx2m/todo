import { ApiProperty } from '@nestjs/swagger';
import { TodoResponseDto } from './todo-response.dto';

export class TodoGraphEdgeDto {
  @ApiProperty({ example: '67e6d0fd2f6b9d3f7d8d1001' })
  prerequisiteId: string;

  @ApiProperty({ example: '67e6d0fd2f6b9d3f7d8d1002' })
  dependentId: string;
}

export class TodoSubgraphDto {
  @ApiProperty({ example: '67e6d0fd2f6b9d3f7d8d1234' })
  rootId: string;

  @ApiProperty({ type: () => TodoResponseDto, isArray: true })
  nodes: TodoResponseDto[];

  @ApiProperty({ type: () => TodoGraphEdgeDto, isArray: true })
  edges: TodoGraphEdgeDto[];
}
